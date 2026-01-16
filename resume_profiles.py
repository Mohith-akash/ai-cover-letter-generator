import re

RESUME_PROFILES = {
    "data_engineer": {
        "name": "Data Engineer",
        "file": "Data_Engineer.html",
        "title_keywords": ["data engineer", "platform engineer", "etl developer", "pipeline engineer", "data infrastructure"],
        "key_skills": ["databricks", "delta lake", "delta", "dbt", "dagster", "azure", "spark", "pyspark", 
                       "streaming", "etl", "elt", "pipeline", "lakehouse", "medallion", "kafka", "airflow",
                       "snowflake", "redshift", "bigquery", "data warehouse", "data platform", "ingestion"],
        "description": "Focus on Databricks, Delta Lake, streaming pipelines, and data infrastructure"
    },
    "analytics_engineer": {
        "name": "Analytics Engineer",
        "file": "Analytics_Engineer.html",
        "title_keywords": ["analytics engineer", "bi engineer", "data modeler"],
        "key_skills": ["dbt", "dimensional modeling", "star schema", "kimball", "metrics layer", 
                       "semantic layer", "looker", "mode", "sigma", "data modeling", "marts"],
        "description": "Focus on dbt, dimensional modeling, semantic layer, metrics"
    },
    "ai_engineer": {
        "name": "AI Engineer",
        "file": "AI_Engineer.html",
        "title_keywords": ["ai engineer", "ml engineer", "machine learning engineer", "llm engineer", 
                           "nlp engineer", "genai", "generative ai"],
        "key_skills": ["llm", "rag", "langchain", "chromadb", "gemini", "gpt", "openai", "vector database",
                       "embeddings", "transformer", "fine-tuning", "prompt engineering", "huggingface"],
        "description": "Focus on RAG systems, LLMs, vector databases, AI applications"
    },
    "data_analyst": {
        "name": "Data Analyst", 
        "file": "Data_Analyst.html",
        "title_keywords": ["data analyst", "business analyst", "reporting analyst", "product analyst", 
                           "insights analyst", "bi analyst"],
        "key_skills": ["tableau", "power bi", "looker", "excel", "google sheets", "stakeholder", 
                       "requirements", "ad-hoc", "reporting", "dashboard"],
        "description": "Focus on SQL analysis, visualization, business insights"
    }
}



def score_job_match(job_text: str, profile_key: str) -> dict:
    profile = RESUME_PROFILES.get(profile_key)
    if not profile:
        return {"score": 0, "matched_skills": [], "matched_roles": []}
    
    job_lower = job_text.lower()
    matched_titles = []
    for title in profile.get("title_keywords", []):
        if title in job_lower:
            matched_titles.append(title)
    matched_skills = []
    for skill in profile.get("key_skills", []):
        # Use word boundary matching for short terms
        if len(skill) <= 3:
            if re.search(rf'\b{re.escape(skill)}\b', job_lower):
                matched_skills.append(skill)
        else:
            if skill in job_lower:
                matched_skills.append(skill)
    
    # Calculate scores
    title_count = len(profile.get("title_keywords", []))
    skill_count = len(profile.get("key_skills", []))
    
    title_score = (len(matched_titles) / title_count * 100) if title_count else 0
    skill_score = (len(matched_skills) / skill_count * 100) if skill_count else 0
    title_bonus = 30 if matched_titles else 0
    
    # Weighted score: titles=50%, skills=50% + title bonus
    total_score = (title_score * 0.5) + (skill_score * 0.5) + title_bonus
    total_score = min(100, total_score)
    
    return {
        "score": round(total_score, 1),
        "matched_skills": matched_skills,
        "matched_roles": matched_titles,
        "profile_name": profile["name"],
        "description": profile["description"]
    }


def get_best_resume(job_text: str) -> tuple:
    all_scores = {}
    
    for profile_key in RESUME_PROFILES:
        result = score_job_match(job_text, profile_key)
        all_scores[profile_key] = result
    
    # Find best match
    best_key = max(all_scores, key=lambda k: all_scores[k]["score"])
    
    return best_key, all_scores


def get_all_scores_sorted(job_text: str) -> list:
    _, all_scores = get_best_resume(job_text)
    
    # Sort by score descending
    sorted_scores = sorted(
        all_scores.items(), 
        key=lambda x: x[1]["score"], 
        reverse=True
    )
    
    return sorted_scores
