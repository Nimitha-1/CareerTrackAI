import requests
from typing import List, Dict
from urllib.parse import quote_plus, urljoin
import re
import os
from bs4 import BeautifulSoup
import time

# ============================================
# CONFIGURATION
# ============================================

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'application/json, text/html',
    'Accept-Language': 'en-US,en;q=0.9',
}


# ============================================
# SOURCE 1: LinkedIn Jobs (Official)
# ============================================

def search_linkedin_jobs(query: str, location: str = "United States", num_results: int = 10) -> List[Dict]:
    """
    Search LinkedIn Jobs (public job postings, no API key needed).
    Uses LinkedIn's public job search.
    """
    jobs = []
    
    try:
        # LinkedIn public job search URL
        base_url = "https://www.linkedin.com/jobs/search"
        
        params = {
            'keywords': query,
            'location': location,
            'position': 1,
            'pageNum': 0
        }
        
        # Build URL
        url = f"{base_url}?keywords={quote_plus(query)}&location={quote_plus(location)}"
        
        print(f"Searching LinkedIn for: {query} in {location}")
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find job cards
            job_cards = soup.find_all('div', class_='base-card')[:num_results]
            
            for card in job_cards:
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    location_elem = card.find('span', class_='job-search-card__location')
                    link_elem = card.find('a', class_='base-card__full-link')
                    
                    if title_elem and link_elem:
                        job = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip() if company_elem else 'N/A',
                            'location': location_elem.text.strip() if location_elem else location,
                            'url': link_elem.get('href', ''),
                            'source': 'LinkedIn',
                            'description': f"Job opening at {company_elem.text.strip() if company_elem else 'company'}",
                            'salary': 'Not specified'
                        }
                        jobs.append(job)
                except Exception as e:
                    continue
        
        print(f"Found {len(jobs)} jobs from LinkedIn")
        
    except Exception as e:
        print(f"LinkedIn error: {e}")
    
    return jobs


# ============================================
# SOURCE 2: Indeed (Official Job Board)
# ============================================

def search_indeed_jobs(query: str, location: str = "United States", num_results: int = 10) -> List[Dict]:
    """
    Search Indeed.com for jobs.
    """
    jobs = []
    
    try:
        base_url = "https://www.indeed.com/jobs"
        params = {
            'q': query,
            'l': location,
            'fromage': 7,  # Last 7 days
        }
        
        url = f"{base_url}?q={quote_plus(query)}&l={quote_plus(location)}"
        
        print(f"Searching Indeed for: {query} in {location}")
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find job cards
            job_cards = soup.find_all('div', class_='job_seen_beacon')[:num_results]
            
            for card in job_cards:
                try:
                    title_elem = card.find('h2', class_='jobTitle')
                    company_elem = card.find('span', class_='companyName')
                    location_elem = card.find('div', class_='companyLocation')
                    
                    # Get job link
                    link = card.find('a', {'data-jk': True})
                    job_id = link.get('data-jk') if link else None
                    
                    if title_elem and job_id:
                        job_url = f"https://www.indeed.com/viewjob?jk={job_id}"
                        
                        job = {
                            'title': title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True) if company_elem else 'N/A',
                            'location': location_elem.get_text(strip=True) if location_elem else location,
                            'url': job_url,
                            'source': 'Indeed',
                            'description': f"Job posting from Indeed.com",
                            'salary': 'See job posting'
                        }
                        jobs.append(job)
                except Exception as e:
                    continue
        
        print(f"Found {len(jobs)} jobs from Indeed")
        
    except Exception as e:
        print(f"Indeed error: {e}")
    
    return jobs


# ============================================
# SOURCE 3: Google Jobs (Aggregator)
# ============================================

def search_google_jobs(query: str, location: str = "United States", num_results: int = 10) -> List[Dict]:
    """
    Search using SerpAPI for Google Jobs results.
    Falls back to direct search if no API key.
    """
    jobs = []
    
    serp_api_key = os.getenv("SERP_API_KEY")
    
    if serp_api_key:
        try:
            url = "https://serpapi.com/search"
            params = {
                'engine': 'google_jobs',
                'q': query,
                'location': location,
                'api_key': serp_api_key,
                'num': num_results
            }
            
            print(f"Searching Google Jobs via SerpAPI: {query}")
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                for job_data in data.get('jobs_results', [])[:num_results]:
                    job = {
                        'title': job_data.get('title', 'N/A'),
                        'company': job_data.get('company_name', 'N/A'),
                        'location': job_data.get('location', location),
                        'url': job_data.get('share_url', job_data.get('apply_link', '#')),
                        'source': 'Google Jobs',
                        'description': job_data.get('description', '')[:300],
                        'salary': job_data.get('salary', 'Not specified')
                    }
                    jobs.append(job)
                
                print(f"Found {len(jobs)} jobs from Google Jobs")
                
        except Exception as e:
            print(f"Google Jobs error: {e}")
    
    return jobs


# ============================================
# SOURCE 4: Company Career Pages (Direct)
# ============================================

TECH_COMPANIES_CAREERS = {
    'Google': 'https://careers.google.com/jobs/results/',
    'Microsoft': 'https://careers.microsoft.com/professionals/us/en/search-results',
    'Amazon': 'https://www.amazon.jobs/en/search',
    'Meta': 'https://www.metacareers.com/jobs',
    'Apple': 'https://jobs.apple.com/en-us/search',
    'Netflix': 'https://jobs.netflix.com/search',
    'Tesla': 'https://www.tesla.com/careers/search',
    'SpaceX': 'https://www.spacex.com/careers',
    'Airbnb': 'https://careers.airbnb.com/',
    'Uber': 'https://www.uber.com/us/en/careers/',
    'Salesforce': 'https://salesforce.wd1.myworkdayjobs.com/External_Career_Site',
}


def search_company_careers(query: str, num_results: int = 5) -> List[Dict]:
    """
    Search company career pages directly.
    This is a simplified version - in production, each company needs custom parsing.
    """
    jobs = []
    
    # For demo, return some structured company job data
    # In production, you'd scrape each company's careers page
    
    query_lower = query.lower()
    relevant_companies = []
    
    # Match query to companies
    if any(word in query_lower for word in ['software', 'engineer', 'developer', 'tech']):
        relevant_companies = ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple']
    elif 'data' in query_lower:
        relevant_companies = ['Google', 'Microsoft', 'Amazon', 'Netflix']
    elif 'machine learning' in query_lower or 'ml' in query_lower or 'ai' in query_lower:
        relevant_companies = ['Google', 'Microsoft', 'Meta', 'Tesla', 'Amazon']
    else:
        relevant_companies = list(TECH_COMPANIES_CAREERS.keys())[:5]
    
    for company in relevant_companies[:num_results]:
        if company in TECH_COMPANIES_CAREERS:
            job = {
                'title': f"{query.title()} at {company}",
                'company': company,
                'location': 'Multiple Locations',
                'url': TECH_COMPANIES_CAREERS[company],
                'source': f'{company} Careers',
                'description': f"Explore {query} opportunities at {company}. Visit their official careers page for current openings.",
                'salary': 'Competitive'
            }
            jobs.append(job)
    
    print(f"Added {len(jobs)} company career page links")
    
    return jobs


# ============================================
# SOURCE 5: RemoteOK (Remote Jobs)
# ============================================

def search_remoteok(query: str, num_results: int = 10) -> List[Dict]:
    """
    Search RemoteOK for remote positions.
    """
    jobs = []
    
    try:
        url = "https://remoteok.com/api"
        
        print(f"Searching RemoteOK for remote: {query}")
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            query_lower = query.lower()
            
            # Skip first element (metadata)
            for item in data[1:]:
                try:
                    position = item.get('position', '').lower()
                    description = item.get('description', '').lower()
                    
                    # Filter by relevance
                    if query_lower in position or any(word in position for word in query_lower.split()):
                        job = {
                            'title': item.get('position', 'Remote Position'),
                            'company': item.get('company', 'N/A'),
                            'location': 'Remote',
                            'url': item.get('url', f"https://remoteok.com/remote-jobs/{item.get('slug', '')}"),
                            'source': 'RemoteOK',
                            'description': (item.get('description', '')[:300]) if item.get('description') else 'Remote opportunity',
                            'salary': f"${item.get('salary_min', 'N/A')}-${item.get('salary_max', 'N/A')}" if item.get('salary_min') else 'Not specified'
                        }
                        jobs.append(job)
                        
                        if len(jobs) >= num_results:
                            break
                except Exception as e:
                    continue
        
        print(f"Found {len(jobs)} jobs from RemoteOK")
        
    except Exception as e:
        print(f"RemoteOK error: {e}")
    
    return jobs


# ============================================
# SOURCE 6: GitHub Jobs
# ============================================

def search_github_jobs(query: str, num_results: int = 10) -> List[Dict]:
    """
    Search GitHub for job postings.
    """
    jobs = []
    
    try:
        url = "https://api.github.com/search/issues"
        params = {
            'q': f'{query} is:issue is:open label:hiring',
            'sort': 'created',
            'order': 'desc',
            'per_page': num_results
        }
        
        print(f"Searching GitHub for: {query}")
        
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            for item in data.get('items', [])[:num_results]:
                job = {
                    'title': item.get('title', 'GitHub Job Posting'),
                    'company': item.get('user', {}).get('login', 'Various Companies'),
                    'location': 'Remote/Various',
                    'url': item.get('html_url', ''),
                    'source': 'GitHub',
                    'description': (item.get('body', '')[:300]) if item.get('body') else 'See posting for details',
                    'salary': 'See posting'
                }
                jobs.append(job)
        
        print(f"Found {len(jobs)} jobs from GitHub")
        
    except Exception as e:
        print(f"GitHub Jobs error: {e}")
    
    return jobs


# ============================================
# MAIN SEARCH FUNCTION
# ============================================

def search_jobs_comprehensive(
    query: str,
    location: str = "United States",
    experience_level: str = "All Levels",
    job_type: List[str] = None,
    num_results: int = 20
) -> List[Dict]:
    """
    Comprehensive job search across multiple official sources.
    
    Priority order:
    1. LinkedIn (official job board)
    2. Indeed (official job board)
    3. Google Jobs (aggregator with company links)
    4. Company Career Pages (direct)
    5. RemoteOK (for remote positions)
    6. GitHub (for tech positions)
    """
    
    all_jobs = []
    results_per_source = max(3, num_results // 6)
    
    print(f"\n{'='*50}")
    print(f"JOB SEARCH: {query}")
    print(f"Location: {location}")
    print(f"Experience: {experience_level}")
    print(f"{'='*50}\n")
    
    # Adjust query for experience level
    if experience_level != "All Levels":
        query = f"{experience_level} {query}"
    
    # 1. LinkedIn Jobs (High Priority)
    try:
        linkedin_jobs = search_linkedin_jobs(query, location, results_per_source)
        all_jobs.extend(linkedin_jobs)
        time.sleep(1)  # Rate limiting
    except Exception as e:
        print(f"LinkedIn failed: {e}")
    
    # 2. Indeed Jobs (High Priority)
    try:
        indeed_jobs = search_indeed_jobs(query, location, results_per_source)
        all_jobs.extend(indeed_jobs)
        time.sleep(1)
    except Exception as e:
        print(f"Indeed failed: {e}")
    
    # 3. Google Jobs (via API if available)
    try:
        google_jobs = search_google_jobs(query, location, results_per_source)
        all_jobs.extend(google_jobs)
        time.sleep(1)
    except Exception as e:
        print(f"Google Jobs failed: {e}")
    
    # 4. Company Career Pages
    try:
        company_jobs = search_company_careers(query, results_per_source)
        all_jobs.extend(company_jobs)
    except Exception as e:
        print(f"Company careers failed: {e}")
    
    # 5. RemoteOK (if location is Remote)
    if location.lower() == "remote":
        try:
            remote_jobs = search_remoteok(query, results_per_source)
            all_jobs.extend(remote_jobs)
            time.sleep(1)
        except Exception as e:
            print(f"RemoteOK failed: {e}")
    
    # 6. GitHub Jobs (for tech roles)
    if any(word in query.lower() for word in ['software', 'developer', 'engineer', 'tech']):
        try:
            github_jobs = search_github_jobs(query, results_per_source)
            all_jobs.extend(github_jobs)
        except Exception as e:
            print(f"GitHub Jobs failed: {e}")
    
    # Deduplicate jobs
    seen_jobs = set()
    unique_jobs = []
    
    for job in all_jobs:
        # Create unique key
        job_key = f"{job.get('title', '').lower()}_{job.get('company', '').lower()}"
        
        if job_key not in seen_jobs:
            seen_jobs.add(job_key)
            unique_jobs.append(job)
    
    print(f"\n{'='*50}")
    print(f"TOTAL UNIQUE JOBS FOUND: {len(unique_jobs)}")
    print(f"{'='*50}\n")
    
    return unique_jobs[:num_results]


def match_jobs_to_skills(jobs: List[Dict], skills_data: Dict) -> List[Dict]:
    """
    Match jobs to user skills and calculate match scores.
    """
    
    # Get all user skills (lowercase for matching)
    user_skills_lower = [s.lower() for s in skills_data.get('technical_skills', [])]
    user_skills_lower.extend([s.lower() for s in skills_data.get('soft_skills', [])])
    
    matched_jobs = []
    
    for job in jobs:
        try:
            # Combine title and description for matching
            job_text = f"{job.get('title', '')} {job.get('description', '')}".lower()
            
            # Count matching skills
            matches = []
            for skill in user_skills_lower:
                # Check if skill appears in job text
                if skill in job_text or any(word in job_text for word in skill.split()):
                    matches.append(skill)
            
            # Calculate match score
            if user_skills_lower:
                match_score = int((len(set(matches)) / len(set(user_skills_lower))) * 100)
            else:
                match_score = 50
            
            # Boost score for experience match
            user_exp = skills_data.get('total_experience', 0)
            job_title_lower = job.get('title', '').lower()
            
            if user_exp >= 5 and ('senior' in job_title_lower or 'lead' in job_title_lower):
                match_score = min(100, match_score + 10)
            elif user_exp < 3 and ('junior' in job_title_lower or 'entry' in job_title_lower):
                match_score = min(100, match_score + 10)
            
            # Add match data to job
            job_copy = job.copy()
            job_copy['matched_skills'] = list(set(matches))[:10]  # Top 10 matches
            job_copy['match_score'] = max(0, min(100, match_score))  # Clamp 0-100
            job_copy['missing_skills'] = [s for s in user_skills_lower if s not in matches][:5]
            
            matched_jobs.append(job_copy)
            
        except Exception as e:
            print(f"Error matching job: {e}")
            job_copy = job.copy()
            job_copy['match_score'] = 0
            matched_jobs.append(job_copy)
    
    # Sort by match score
    matched_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
    
    return matched_jobs


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    # Test the job search
    print("Testing job search...\n")
    
    jobs = search_jobs_comprehensive(
        query="Python Developer",
        location="San Francisco, CA",
        num_results=15
    )
    
    print(f"\n\nFound {len(jobs)} jobs:")
    for i, job in enumerate(jobs[:5], 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source']}")
        print(f"   URL: {job['url'][:100]}...")