import os
import glob
import pickle
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

KB_PATH = "knowledge_base"
INDEX_FILE = "vector_index.faiss"
CHUNKS_FILE = "chunks.pkl"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# globals
vector_index = None
chunks = []


def load_text_from_file(file_path):
    """Extract text from .txt or .pdf files"""
    try:
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        elif ext == ".pdf":
            text = ""
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
            return text

        return ""
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return ""


def split_into_chunks(text, max_length=300):
    """Split text into chunks of approximately max_length words"""
    words = text.split()
    result = []
    current = []

    for w in words:
        current.append(w)
        if len(current) >= max_length:
            result.append(" ".join(current))
            current = []

    if current:
        result.append(" ".join(current))

    return result


def build_embeddings():
    """Build vector embeddings from all files in knowledge base"""
    global vector_index, chunks

    try:
        # Get all files from knowledge base
        files = glob.glob(os.path.join(KB_PATH, "*"))
        if not files:
            print("⚠️ No files found in KB.")
            return False

        all_chunks = []

        # Process each file
        for file in files:
            print(f"📄 Processing: {file}")
            text = load_text_from_file(file)
            
            if not text.strip():
                print(f"⚠️ No text extracted from {file}")
                continue

            # Split into chunks
            parts = split_into_chunks(text)
            all_chunks.extend(parts)
            print(f"   ✅ Extracted {len(parts)} chunks")

        if not all_chunks:
            print("⚠️ No text found in uploaded files.")
            return False

        print(f"\n🔄 Creating embeddings for {len(all_chunks)} chunks...")
        
        # Create embeddings
        embeddings = embedding_model.encode(all_chunks, show_progress_bar=True)
        embeddings = np.array(embeddings, dtype=np.float32)

        # Build FAISS index
        vector_index = faiss.IndexFlatL2(embeddings.shape[1])
        vector_index.add(embeddings)
        
        # Save index
        faiss.write_index(vector_index, INDEX_FILE)
        
        # Save chunks persistently
        with open(CHUNKS_FILE, "wb") as f:
            pickle.dump(all_chunks, f)
        
        # Update global chunks
        chunks = all_chunks

        print(f"✅ Embeddings built successfully: {len(all_chunks)} chunks indexed")
        return True
        
    except Exception as e:
        print(f"❌ Error building embeddings: {e}")
        return False


def load_existing_index():
    """Load existing vector index and chunks from disk"""
    global vector_index, chunks
    
    try:
        if os.path.exists(INDEX_FILE) and os.path.exists(CHUNKS_FILE):
            print("📂 Loading existing index and chunks...")
            vector_index = faiss.read_index(INDEX_FILE)
            
            with open(CHUNKS_FILE, "rb") as f:
                chunks = pickle.load(f)
            
            print(f"✅ Loaded {len(chunks)} chunks from disk")
            return True
        else:
            print("⚠️ No existing index found")
            return False
    except Exception as e:
        print(f"❌ Error loading index: {e}")
        return False


def query_vector_store(query, top_k=3):
    """Query the vector store to find relevant chunks"""
    global vector_index, chunks

    try:
        # Load index if not in memory
        if vector_index is None or len(chunks) == 0:
            if not load_existing_index():
                print("⚠️ No index available. Please upload documents first.")
                return []

        # Create query embedding
        query_vec = embedding_model.encode([query])
        query_vec = np.array(query_vec, dtype=np.float32)

        # Search for similar chunks
        D, I = vector_index.search(query_vec, min(top_k, len(chunks)))

        results = []
        for idx in I[0]:
            if 0 <= idx < len(chunks):
                results.append(chunks[idx])
        
        print(f"🔍 Found {len(results)} relevant chunks for query")
        return results
        
    except Exception as e:
        print(f"❌ Error querying vector store: {e}")
        return []


def get_index_info():
    """Get information about the current index"""
    global vector_index, chunks
    
    if vector_index is None or len(chunks) == 0:
        load_existing_index()
    
    return {
        "num_chunks": len(chunks),
        "index_exists": vector_index is not None,
        "sample_chunk": chunks[0][:100] + "..." if chunks else "No chunks available"
    }