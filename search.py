import requests
import os

TAVILY_API_URL = "https://api.tavily.com/search"


def search_company_mission(company_name: str, api_key: str = None) -> dict:
    api_key = api_key or os.getenv("TAVILY_API_KEY")
    
    if not api_key:
        return {"success": False, "error": "No Tavily API key"}
    
    queries = [
        f'"{company_name}" mission statement values culture',
        f'"{company_name}" company vision goals achievements'
    ]
    
    all_results = []
    
    for query in queries:
        try:
            response = requests.post(
                TAVILY_API_URL,
                json={
                    "api_key": api_key,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 3,
                    "include_answer": True,
                    # Exclude negative keywords
                    "exclude_domains": ["glassdoor.com"],
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                all_results.append(data.get("answer", ""))
        except Exception as e:
            print(f"[WARN] Tavily search failed for query {query!r}: {e}")
    
    # Filter out None values first
    all_results = [r for r in all_results if r is not None]
    combined_text = " ".join(all_results)
    
    negative_keywords = [
        "layoff", "lawsuit", "scandal", "controversy", "fired", 
        "accused", "failed", "bankrupt", "decline", "criticized"
    ]
    
    sentences = combined_text.split(".")
    positive_sentences = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if not any(neg in sentence_lower for neg in negative_keywords):
            if len(sentence.strip()) > 20:  # Skip very short sentences
                positive_sentences.append(sentence.strip())
    
    positive_text = ". ".join(positive_sentences[:5])  # Limit to 5 sentences
    
    return {
        "success": True if positive_text else False,
        "mission_values": positive_text,
        "raw_results": all_results
    }


def extract_company_alignment(company_research: str, user_skills: list, cerebras_client) -> str:
    """
    Generate a company alignment statement using LLM.
    Creates: "I'm drawn to [Company]'s commitment to [value]..."
    """
    if not cerebras_client or not company_research:
        return ""
    
    skills_text = ", ".join([s["skill"] for s in user_skills[:5]]) if user_skills else "data engineering"
    
    prompt = f"""Based on this company research, write ONE sentence about how you align with the company's mission.

COMPANY RESEARCH:
{company_research[:500]}

MY SKILLS:
{skills_text}

Write ONE sentence in this format:
"I'm drawn to [Company]'s commitment to [specific value/goal]. My experience with [relevant skill/project] aligns with this mission."

Keep it specific and authentic. Only use information from the research.

ALIGNMENT SENTENCE:"""

    try:
        response = cerebras_client.chat.completions.create(
            model="llama-3.1-8b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return ""

