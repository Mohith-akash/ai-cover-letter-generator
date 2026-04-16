import requests
from langdetect import detect, LangDetectException

# Jina Reader API
JINA_READER_URL = "https://r.jina.ai/"


def fallback_scrape(url: str) -> dict:
    try:
        from bs4 import BeautifulSoup
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = '\n'.join(lines)
            
            return {"success": True, "content": text[:15000]}  # Limit size
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def scrape_job_url(url: str, jina_api_key: str = None) -> dict:
    # Try Jina first
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        if jina_api_key:
            headers["Authorization"] = f"Bearer {jina_api_key}"
        
        response = requests.get(
            f"{JINA_READER_URL}{url}",
            headers=headers,
            timeout=15  # Short timeout for Jina
        )
        
        if response.status_code == 200 and len(response.text) > 100:
            return {
                "success": True,
                "content": response.text,
                "url": url,
                "method": "jina"
            }
    except Exception as e:
        print(f"[WARN] Jina scrape failed for {url}, falling back to direct scrape: {e}")
    
    # Fallback to direct scraping
    print("Jina failed, trying direct scrape...")
    result = fallback_scrape(url)
    if result["success"]:
        result["url"] = url
        result["method"] = "fallback"
    return result


def detect_language(text: str) -> str:
    try:
        # Use first 1000 chars for detection (faster)
        sample = text[:1000] if len(text) > 1000 else text
        lang = detect(sample)
        return lang
    except LangDetectException:
        return "en"  # Default to English if detection fails


def translate_with_llm(text: str, source_lang: str, cerebras_client) -> str:
    if source_lang == "en":
        return text
    
    prompt = f"""Translate the following job posting from {source_lang} to English.

IMPORTANT RULES:
- Keep technical terms in English (Spark, Python, SQL, dbt, Databricks, etc.)
- Keep company names unchanged
- Keep acronyms unchanged (API, ETL, ML, AI, etc.)
- Produce natural, professional English

TEXT TO TRANSLATE:
{text}

ENGLISH TRANSLATION:"""

    try:
        response = cerebras_client.chat.completions.create(
            model="llama-3.1-8b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Translation error: {e}"


def extract_job_info(text: str, cerebras_client) -> dict:
    if not cerebras_client:
        return {"company": "", "title": "", "location": ""}
    
    prompt = """Extract the following from this job posting. Return ONLY a JSON object with these fields:
- company: the company name
- title: the job title
- location: city and country

Job posting:
""" + text[:3000] + """

Return ONLY valid JSON like: {"company": "Google", "title": "Data Engineer", "location": "London, UK"}
JSON:"""

    try:
        response = cerebras_client.chat.completions.create(
            model="llama-3.1-8b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0
        )
        result = response.choices[0].message.content.strip()
        
        # Parse JSON
        import json
        # Find JSON in response
        start = result.find("{")
        end = result.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(result[start:end])
    except Exception as e:
        print(f"Extract error: {e}")
    
    return {"company": "", "title": "", "location": ""}


def process_job_input(input_text: str, jina_api_key: str = None, cerebras_client=None) -> dict:
    # Check if input is URL
    is_url = input_text.strip().startswith(("http://", "https://"))
    
    if is_url:
        # Scrape the URL
        result = scrape_job_url(input_text.strip(), jina_api_key)
        if not result["success"]:
            return result
        content = result["content"]
    else:
        content = input_text
    
    # Detect language
    lang = detect_language(content)
    
    # Translate if not English
    if lang != "en" and cerebras_client:
        content = translate_with_llm(content, lang, cerebras_client)
    
    # Extract job info
    job_info = extract_job_info(content, cerebras_client)
    
    return {
        "success": True,
        "content": content,
        "original_language": lang,
        "was_translated": lang != "en",
        "is_url": is_url,
        "job_info": job_info
    }
