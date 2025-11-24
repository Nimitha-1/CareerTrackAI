import requests
import os
from urllib.parse import quote_plus


def live_web_search(query):
    """
    Perform a live web search using available search APIs.
    Tries multiple providers in order of preference.
    """
    
    # Try SerpAPI first (if API key is available)
    serp_api_key = os.getenv("SERP_API_KEY")
    if serp_api_key:
        result = search_with_serpapi(query, serp_api_key)
        if result:
            return result
    
    # Fallback to DuckDuckGo (free, no API key needed)
    result = search_with_duckduckgo(query)
    if result:
        return result
    
    return "Web search is not configured. Please add SERP_API_KEY to your .env file or check your internet connection."


def search_with_serpapi(query, api_key):
    """
    Search using SerpAPI (Google Search API)
    Get your API key from: https://serpapi.com/
    """
    try:
        url = f"https://serpapi.com/search?q={quote_plus(query)}&api_key={api_key}"
        resp = requests.get(url, timeout=10)

        if resp.status_code != 200:
            print(f"SerpAPI returned status code: {resp.status_code}")
            return None

        data = resp.json()
        
        # Check for error in response
        if "error" in data:
            print(f"SerpAPI error: {data['error']}")
            return None
            
        if "organic_results" not in data or len(data["organic_results"]) == 0:
            return "No search results found."

        results = data["organic_results"][:3]

        output = "🌐 **Web Search Results:**\n\n"
        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            snippet = r.get("snippet", "No description available.")
            link = r.get("link", "")
            output += f"**{i}. {title}**\n{snippet}\n"
            if link:
                output += f"🔗 {link}\n"
            output += "\n"

        return output

    except requests.exceptions.Timeout:
        print("SerpAPI request timed out")
        return None
    except Exception as e:
        print(f"SerpAPI search error: {e}")
        return None


def search_with_duckduckgo(query):
    """
    Search using DuckDuckGo Instant Answer API (free, no API key needed)
    Limited but useful for quick searches
    """
    try:
        # DuckDuckGo Instant Answer API
        url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json"
        resp = requests.get(url, timeout=10)

        if resp.status_code != 200:
            print(f"DuckDuckGo returned status code: {resp.status_code}")
            return None

        data = resp.json()
        
        output = "🌐 **Web Search Results (DuckDuckGo):**\n\n"
        
        # Get abstract if available
        if data.get("Abstract"):
            output += f"**Summary:**\n{data['Abstract']}\n\n"
            if data.get("AbstractURL"):
                output += f"🔗 Source: {data['AbstractURL']}\n\n"
        
        # Get related topics
        if data.get("RelatedTopics"):
            topics = data["RelatedTopics"][:3]
            output += "**Related Information:**\n"
            for i, topic in enumerate(topics, 1):
                if isinstance(topic, dict) and "Text" in topic:
                    text = topic.get("Text", "")
                    first_url = topic.get("FirstURL", "")
                    if text:
                        output += f"{i}. {text}\n"
                        if first_url:
                            output += f"   🔗 {first_url}\n"
            output += "\n"
        
        # If we got some content, return it
        if len(output) > 100:  # More than just the header
            return output
        
        # If no substantial results, try alternative approach
        return search_with_wikipedia(query)

    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
        return None


def search_with_wikipedia(query):
    """
    Fallback: Search Wikipedia API (free, no API key needed)
    """
    try:
        # Wikipedia API search
        search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={quote_plus(query)}&limit=3&format=json"
        resp = requests.get(search_url, timeout=10)
        
        if resp.status_code != 200:
            return None
            
        data = resp.json()
        
        if len(data) < 4 or not data[1]:
            return "No Wikipedia results found."
        
        titles = data[1]
        descriptions = data[2]
        urls = data[3]
        
        output = "🌐 **Wikipedia Search Results:**\n\n"
        
        for i, (title, desc, url) in enumerate(zip(titles, descriptions, urls), 1):
            output += f"**{i}. {title}**\n"
            if desc:
                output += f"{desc}\n"
            output += f"🔗 {url}\n\n"
        
        return output
        
    except Exception as e:
        print(f"Wikipedia search error: {e}")
        return None


def test_web_search():
    """
    Test function to verify web search is working
    """
    print("Testing web search functionality...\n")
    
    test_queries = [
        "Python programming language",
        "Machine learning basics",
        "Current weather"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        result = live_web_search(query)
        print(result)
        print("-" * 50)


if __name__ == "__main__":
    # Run test when script is executed directly
    test_web_search()