# AI Cover Letter Generator

> Paste a job URL, get a tailored cover letter in 30 seconds. Auto-selects resume, researches company, generates A-grade content.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What It Does

**Paste job URL → Get tailored cover letter**

- 🏆 **Auto CV Selection** - 4 main resume types + 10+ similar role mappings, picks best match with % score
- 🔍 **Company Research** - Tavily API pulls mission/values, filters out negatives (layoffs, scandals)
- ✨ **3 Tone Options** - Confident, Formal, or Conversational depending on company culture
- 🎯 **90+ Tool Mappings** - Shows your skills correctly: "I use Dagster (Airflow-style)"
- 📊 **A-F Quality Scoring** - Professionalism checks, grammar, no AI tells
- 🌍 **Works Globally** - EU, US, Canada, Asia - any job posting, any language (auto-translates)
- 📋 **Export Ready** - HTML for PDF, plain text for LinkedIn/Indeed/Workday portals

## Tech Stack

```
Python 3.11+ • Streamlit
Cerebras (Llama 3.1) • Tavily • Jina Reader
```

**Why this stack:**
- Cerebras: Free tier, fast inference
- Tavily: Company research without scraping
- Streamlit: Local deployment, no backend

## Quick Start

```bash
git clone https://github.com/Mohith-akash/ai-cover-letter-generator.git
cd ai-cover-letter-generator
pip install -r requirements.txt

cp .env.example .env      # Add API keys
cp config.py.example config.py   # Add your info

streamlit run app.py
```

**API Keys (all free tier):** [Cerebras](https://cloud.cerebras.ai) • [Tavily](https://tavily.com) • [Jina](https://jina.ai/reader)

## Supported Roles

| Main Categories | Similar Roles Included |
|----------------|----------------------|
| **Data Engineer** | Platform Engineer, ETL Developer, Pipeline Engineer, Data Infrastructure |
| **Analytics Engineer** | BI Developer, Data Modeler, Metrics Engineer |
| **AI Engineer** | ML Engineer, LLM Engineer, NLP Engineer, GenAI Developer |
| **Data Analyst** | Business Analyst, Product Analyst, Insights Analyst, BI Analyst |

*More roles can be added by editing `resume_profiles.py`*

## Key Features

### Tone Selection
- **Confident** - Startups, tech companies ("I shipped...")
- **Formal** - Enterprise, banking, insurance, EU companies
- **Conversational** - Creative agencies, smaller teams

### Smart Skill Matching
90+ tool alternatives mapped:
- Airflow → Dagster, Prefect
- Tableau → Power BI, Looker
- Snowflake → Databricks
- dbt → Dataform, SQLMesh

Cover letter shows: "I use Dagster (Airflow-style workflow orchestration)"

### Resume-Specific Keywords
Different keywords bolded based on matched resume:
- **Data Engineer**: Databricks, Delta Lake, dbt, Spark, SQL
- **AI Engineer**: LLM, RAG, LangChain, embeddings
- **Analytics Engineer**: Power BI, dimensional modeling, metrics
- **Data Analyst**: Excel, Tableau, SQL, visualization

### Quality Checks
- ✓ Grammar validation (no sentence fragments)
- ✓ AI phrase detection ("seasoned", "leverage", "synergy")
- ✓ Metrics present (numbers > buzzwords)
- ✓ Length appropriate
- ✓ Professional closing

## How It Works

1. **Scrape** - Jina Reader extracts job posting
2. **Translate** - Auto-detects language, translates if needed
3. **Match** - Keyword matching finds best resume (4 types)
4. **Research** - Tavily finds company mission/values (positives only)
5. **Generate** - Cerebras LLM creates opening paragraph with your metrics
6. **Review** - A-F professionalism grade with suggestions
7. **Export** - HTML (→ PDF) or plain text for job portals

## Project Structure

```
├── app.py              # Streamlit UI + workflow
├── generator.py        # LLM prompts + HTML template
├── skills.py           # 90+ tool mappings + project data
├── resume_profiles.py  # 4 CV types + scoring
├── search.py           # Tavily company research
├── review.py           # A-F scoring logic
└── scraper.py          # Jina Reader integration
```

## Why I Built This

Applying to international roles across Europe, US, and Canada - each company wants different things:
- Some want formal tone (banks, insurance)
- Some want confident/direct (startups)
- Tool requirements vary (Airflow vs Dagster, Tableau vs Power BI)
- Each cover letter needed to be customized

Writing 100+ unique cover letters manually, editing one by one, switching formats for different roles - it was painful. This automates the repetitive parts while keeping each letter personalized with company research and your actual metrics.

## Extending

Add new resume types in `resume_profiles.py`:
```python
"new_role": {
    "name": "New Role",
    "title_keywords": ["new role", "similar role"],
    "key_skills": ["skill1", "skill2"],
}
```

Add tool alternatives in `skills.py`:
```python
TOOL_ALTERNATIVES = {
    "job_tool": ["your_tool1", "your_tool2"],
}
```

## License

MIT - Use it, fork it, customize it for your job search.

## Author

**Mohith Akash Saravanan**  
[LinkedIn](https://linkedin.com/in/mohith-akash) • [GitHub](https://github.com/Mohith-akash)

---

If this helps you land interviews, ⭐ the repo!
