import re
from datetime import datetime

from config import PROFILE

# Cover letter templates by tone
TONE_PROMPTS = {
    "confident": "Write in a confident, direct tone. No hedging words. Sound like someone who has proven results.",
    "formal": "Write in a professional, formal tone suitable for traditional companies.",
    "conversational": "Write in a friendly, approachable tone. Sound like a real person, not corporate.",
}

# Anti-AI-tells instructions - much stronger
QUALITY_RULES = """
BANNED PHRASES (DO NOT USE ANY OF THESE):
- "seasoned" / "proven track record" / "extensive experience"
- "leverage" / "utilize" / "facilitate" / "synergy" / "streamlined"
- "I'm excited" / "I'm thrilled" / "I'm passionate" / "I'm eager"
- "I believe I would be" / "I am confident that"
- "As a [job title]" (don't start with this)
- "proven results" / "track record" / "extensive"
- "expertise" / "proficiency" / "proficient"
- em-dashes (—)

STYLE RULES:
- Start with what you BUILT, not who you are
- Use numbers: "processed 16M rows" not "processed large datasets"
- Short sentences. Under 15 words each.
- Sound like you're texting a friend who asked about your work
- Be specific, be direct, be human
"""


def generate_cover_letter(
    job_info: dict,
    matched_skills: list,
    projects: list,
    tone: str,
    cerebras_client,
    transferable_skills: list = None
) -> str:
    """
    Generate a tailored cover letter using Cerebras LLM.
    """
    
    # Build skill match section
    skill_matches = "\n".join([
        f"- {s['skill'].title()}: {s['proof']}" 
        for s in matched_skills[:5]
    ])
    
    # Build projects section
    project_highlights = "\n".join([
        f"- {p['name']}: {p['description']} ({p['metrics']})"
        for p in projects[:2]
    ])
    
    transferable_section = ""
    if transferable_skills:
        transferable_lines = []
        for t in transferable_skills[:2]:
            # Frame it as YOUR skill, not theirs
            transferable_lines.append(
                f"- I use {t['you_have'].title()} (similar to {t['job_needs'].title()} that job mentions)"
            )
        transferable_section = "\n\nMY EQUIVALENT TOOLS:\n" + "\n".join(transferable_lines)
    
    tone_instruction = TONE_PROMPTS.get(tone, TONE_PROMPTS["confident"])
    
    prompt = f"""Write a powerful opening paragraph for a cover letter that immediately grabs attention.

JOB:
- Company: {job_info.get('company', 'the company')}
- Role: {job_info.get('title', 'the position')}

MY WORK (reference these - these are MY projects):
{skill_matches}
{project_highlights}
{transferable_section}

{QUALITY_RULES}

HOOK EXAMPLES (study these patterns):

BAD HOOK (too generic):
"I am writing to express my interest in the Data Engineer position. I have experience with data pipelines and warehousing."

BAD HOOK (grammar error - sentence fragment):
"16 million rows of data processed with 90% latency reduction on Databricks, where I built a serverless pipeline."

GOOD HOOK (complete sentence, leads with I + verb):
"I built a data warehouse processing 16 million rows with 90% latency reduction. My serverless ELT pipeline on Databricks ingests 100K+ daily events with <500ms latency."

EXCELLENT HOOK (bold statement then complete sentence):
"16 million rows. That's the scale of the Global News Intelligence Platform I built from scratch using Databricks, achieving 90% latency reduction through serverless ELT processing."

{tone_instruction}

CRITICAL HOOK RULES:
- Every sentence MUST be grammatically complete (Subject + Verb)
- If starting with a number, follow with: ". That's the [noun] I [verb]..."
- OR start with "I [verb]" for guaranteed grammar correctness
- LEAD with your biggest/most impressive number or achievement (16M rows, 100K events, <500ms latency, 90% reduction)
- NO generic intros like "I am writing to..." or "I am excited to..."
- First sentence = IMMEDIATE value (numbers, scale, impact)
- Each sentence = different project or achievement
- Make them think "this person ships real stuff" within 5 seconds
- Output ONLY the paragraph text. NO explanations, NO meta-commentary.
- Do NOT repeat the same achievement or metric twice
- Do NOT end with generic statements like "These projects showcase..." or "This demonstrates..."
- Only mention tools I ACTUALLY USE (Databricks, Dagster, dbt, Azure Event Hub, Power BI, etc)
- 2-3 sentences MAXIMUM. Keep it punchy and powerful.
- Use "I" not "We" or "Our"

OPENING:"""

    try:
        response = cerebras_client.chat.completions.create(
            model="llama-3.1-8b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7  # Lower temp for more focused output
        )
        result = response.choices[0].message.content.strip()
        
        # Post-process: Remove any meta-commentary
        # Remove "Here's..." prefix
        if result.lower().startswith("here"):
            lines = result.split("\n")
            result = "\n".join(lines[1:]).strip() if len(lines) > 1 else result
        
        # Remove (Note:...) suffix
        if "(note:" in result.lower():
            result = result[:result.lower().find("(note:")].strip()
        
        # Remove trailing parenthetical comments
        if result.endswith(")"):
            last_paren = result.rfind("(")
            if last_paren > len(result) // 2:  # Only if in last half
                result = result[:last_paren].strip()
        
        # Remove surrounding quotation marks if present
        if result.startswith('"') and result.endswith('"'):
            result = result[1:-1].strip()
        elif result.startswith("'") and result.endswith("'"):
            result = result[1:-1].strip()
        
        return result
    except Exception as e:
        return f"Error generating: {e}"


def post_process_text(text: str) -> str:
    # Replace em-dashes with commas
    text = text.replace("—", ", ")
    text = text.replace("–", ", ")
    
    # Remove common AI phrases
    ai_phrases = [
        "I'm excited to",
        "I'm thrilled to",
        "I'm passionate about",
        "I'm eager to",
        "I believe I would be",
        "I am confident that",
        "leverage my",
        "utilize my",
        "synergy",
    ]
    
    for phrase in ai_phrases:
        text = text.replace(phrase, "I")
        text = text.replace(phrase.lower(), "I")
    
    return text


def build_full_cover_letter(
    opening: str,
    job_info: dict,
    matched_skills: list,
    projects: list,
    company_research: str = "",
    cerebras_client = None,
    resume_type: str = "data_engineer"
) -> str:
    """
    Build the complete cover letter HTML.
    NEW: Includes company alignment paragraph if research available.
    NEW: Resume-specific keyword bolding.
    """
    
    # Post-process opening
    opening = post_process_text(opening)
    
    # Format date
    date = datetime.now().strftime("%d %B %Y")
    
    core_tech = ["Databricks", "Delta Lake", "dbt", "Dagster", "Azure Event Hub", "Power BI", "Python", "Polars"]
    tech_list = ", ".join(core_tech)
    
    transferable_html = ""
    if matched_skills:
        from skills import TOOL_ALTERNATIVES
        
        # Get list of skills user actually has
        user_skills_lower = [s["skill"].lower() for s in matched_skills]
        
        # Find which job requirements user has alternatives for
        transferable_dict = {}  # {user_tool: [job_tools]}
        
        for job_skill, user_alternatives in TOOL_ALTERNATIVES.items():
            # Check if job asks for this skill
            job_skill_lower = job_skill.lower()
            
            # Only show if user DOESN'T have the exact job skill
            if job_skill_lower in user_skills_lower:
                continue  # Skip - user already has what job wants
            
            # Check if user has any alternative
            for alt in user_alternatives:
                if alt.lower() in user_skills_lower:
                    # User has an alternative!
                    if alt not in transferable_dict:
                        transferable_dict[alt] = []
                    transferable_dict[alt].append(job_skill)
                    break  # Only add once per job skill
        
        # Format: "I use dbt (Dataform-style, SQLMesh-style)"
        transferable_items = []
        for user_tool, job_tools in transferable_dict.items():
            if len(job_tools) == 1:
                transferable_items.append(
                    f"I use <strong>{user_tool.title()}</strong> <strong>({job_tools[0].title()}-style)</strong>"
                )
            else:
                # Multiple alternatives - group them
                job_tools_str = ", ".join([f"{t.title()}-style" for t in job_tools[:2]])  # Max 2
                transferable_items.append(
                    f"I use <strong>{user_tool.title()}</strong> <strong>({job_tools_str})</strong>"
                )
        
        if transferable_items:
            transferable_html = "<p class='body-text'>" + "; ".join(transferable_items[:2]) + ".</p>\n"
    
    # Generate company alignment paragraph if research available
    alignment_paragraph = ""
    if company_research and cerebras_client:
        from search import extract_company_alignment
        alignment = extract_company_alignment(company_research, matched_skills, cerebras_client)
        if alignment:
            alignment_paragraph = f"<p class='body-text'>{alignment}</p>\n"  # Added class for spacing
    
    # Resume-specific keywords for bolding
    RESUME_KEYWORDS = {
        "data_engineer": ["Databricks", "Delta Lake", "Delta", "dbt", "Dagster", "Azure Event Hub", "Azure", "Spark", "SQL", "Python", "streaming", "ELT", "ETL", "pipeline", "lakehouse", "Polars"],
        "analytics_engineer": ["dbt", "SQL", "Power BI", "dimensional modeling", "star schema", "Looker", "Streamlit", "Python", "metrics", "KPIs", "dashboards"],
        "ai_engineer": ["LLM", "RAG", "LangChain", "ChromaDB", "Gemini", "vector", "embeddings", "Python", "semantic search", "Streamlit"],
        "data_analyst": ["SQL", "Excel", "Power BI", "Tableau", "Python", "visualization", "dashboard", "analysis", "Streamlit"]
    }
    
    # Get keywords for this resume type
    resume_keywords = RESUME_KEYWORDS.get(resume_type, RESUME_KEYWORDS["data_engineer"])
    
    # Bold matched skills in text
    def bold_keywords(text, matched_skills, resume_keywords):
        """Bold important keywords and matched skills in text."""
        # Combine matched skills + resume-specific keywords
        keywords = [s["skill"] for s in matched_skills] + resume_keywords
        keywords = list(set([k.lower() for k in keywords]))  # Unique, lowercase
        
        for keyword in keywords:
            # Case-insensitive replace with bold
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            text = pattern.sub(lambda m: f"<strong>{m.group()}</strong>", text, count=1)  # Only first occurrence
        return text
    
    # Bold opening paragraph keywords
    opening_bolded = bold_keywords(opening, matched_skills, resume_keywords)
    
    # Build projects HTML - Show all 3 core projects with bolded tech
    projects_html = ""
    for p in projects:  # Changed from projects[:2] to show all 3
        desc_bolded = bold_keywords(p["description"], matched_skills, resume_keywords)
        projects_html += f'<li><span class="project-name">{p["name"]}</span> - {desc_bolded}</li>\n'
    
    # Generate role-specific custom closing
    role_title = job_info.get('title', 'this role').lower()
    company = job_info.get('company', 'your team')
    
    # Determine role type for custom closing
    if any(word in role_title for word in ['ai', 'llm', 'ml', 'machine learning', 'genai']):
        custom_closing = f"I'd love to discuss how my RAG system experience and LLM integration work can contribute to {company}'s AI initiatives."
    elif any(word in role_title for word in ['data engineer', 'platform', 'pipeline', 'infrastructure']):
        custom_closing = f"I'd be excited to explore how my experience with real-time pipelines and lakehouse architecture can help scale {company}'s data infrastructure."
    elif any(word in role_title for word in ['analytics', 'bi', 'business intelligence']):
        custom_closing = f"I'd welcome the opportunity to discuss how my dimensional modeling and dashboard experience can drive insights at {company}."
    else:
        custom_closing = f"I'd be happy to discuss how my data engineering experience aligns with {job_info.get('title', 'this role')} at {company}."
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cover Letter - {job_info.get('title', 'Application')} - {job_info.get('company', 'Company')}</title>
    <style>
        @page {{ size: A4; margin: 0.5in 0.5in 0.4in 0.5in; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ background: #ffffff; }}
        body {{
            font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
            font-size: 10.5pt;
            line-height: 1.45;  /* Reduced to fit on 1 page */
            color: #1a1a1a;
            background: #ffffff;
            max-width: 800px;
            margin: 0 auto;
            padding: 0;  /* Removed padding */
        }}
        .header {{
            text-align: center;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #2c5282;
        }}
        .name {{
            font-size: 20pt;
            font-weight: 700;
            color: #1a365d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .contact {{ font-size: 9.5pt; color: #4a5568; }}
        .contact a {{ color: #2b6cb0; text-decoration: none; }}
        .date {{ margin-bottom: 12px; margin-top: 12px; }}
        .recipient {{ margin-bottom: 12px; line-height: 1.4; }}
        .subject {{ font-weight: 700; color: #1a365d; margin-bottom: 12px; font-size: 11pt; }}
        .salutation {{ margin-bottom: 12px; }}
        .body-text {{ margin-bottom: 10px; text-align: justify; line-height: 1.5; }}
        .body-text strong {{ color: #2c5282; font-weight: 700; }}  /* Bold keywords in blue */
        .section-title {{ font-weight: 700; color: #2c5282; margin-bottom: 6px; margin-top: 12px; font-size: 10.5pt; }}
        .projects {{ margin: 8px 0 12px 20px; line-height: 1.45; }}
        .projects li {{ margin-bottom: 6px; }}
        .projects strong {{ color: #2c5282; }}  /* Bold tech in projects */
        .project-name {{ font-weight: 700; color: #2c5282; }}
        .highlight-label {{ font-weight: 700; color: #2c5282; }}
        .tech-stack {{ background: #f0f4f8; padding: 6px 10px; border-radius: 4px; margin: 10px 0; border-left: 3px solid #2c5282; }}
        .signature {{ font-weight: 600; color: #2c5282; margin-top: 4px; }}
        @media print {{
            html, body {{ -webkit-print-color-adjust: exact !important; padding: 0; margin: 0; }}
        }}
    </style>
</head>
<body>

<!-- Removed top spacer div -->

<header class="header">
    <div class="name">{PROFILE['name'].upper()}</div>
    <div class="contact">
        {PROFILE['location']} | {PROFILE['phone']} | {PROFILE['email']}<br>
        <a href="https://{PROFILE['linkedin']}">{PROFILE['linkedin']}</a> | 
        <a href="https://{PROFILE['github']}">{PROFILE['github']}</a>
    </div>
</header>

<div class="date">{date}</div>

<div class="recipient">
    Hiring Manager<br>
    {job_info.get('company', '[COMPANY]')}<br>
    {job_info.get('location', '[LOCATION]')}
</div>

<div class="subject">Re: Application for {job_info.get('title', '[POSITION]')}</div>

<div class="salutation">Dear Hiring Manager,</div>

<p class="body-text">{opening_bolded}</p>

<p class="section-title">Here's what I've built:</p>

<ul class="projects">
{projects_html}
</ul>

<div class="tech-stack">
    <span class="highlight-label">Tech stack:</span> <strong>{tech_list}</strong>
</div>

{transferable_html}

{alignment_paragraph}

<p class="body-text">
    I am based in Germany with <strong>EU work authorization (Chancenkarte)</strong> and available immediately. I have {PROFILE['english_level']}.
</p>

<p class="body-text">{custom_closing}</p>

<div style="margin-top: 14px;">Cheers,</div>
<div class="signature">{PROFILE['name']}</div>

<div style="margin-top: 30px; font-size: 7pt; color: #718096; text-align: justify; border-top: 1px solid #e2e8f0; padding-top: 6px;">
    I agree to the processing of personal data provided in this document for realising the recruitment process pursuant to the Personal Data Protection Act of 10 May 2018 (Journal of Laws 2018, item 1000) and in agreement with Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation).
</div>

</body>
</html>"""
    
    return html
