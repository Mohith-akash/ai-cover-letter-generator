import re


def review_cover_letter(text: str) -> dict:
    issues = []
    score = 100  # Start at 100 and deduct for issues
    
    # Clean HTML if present
    clean_text = re.sub(r'<[^>]+>', '', text)
    
    # Word count check (ideal: 250-400 words)
    words = clean_text.split()
    word_count = len(words)
    
    if word_count < 200:
        issues.append({"type": "length", "message": "Too short - add more details", "severity": "warning"})
        score -= 10
    elif word_count > 500:
        issues.append({"type": "length", "message": "Too long - consider trimming", "severity": "warning"})
        score -= 5
    else:
        issues.append({"type": "length", "message": f"Good length ({word_count} words)", "severity": "pass"})
    
    # AI-sounding phrases detection
    ai_phrases = [
        ("I'm excited", "Remove cliché opening"),
        ("I'm thrilled", "Remove cliché opening"),
        ("I'm passionate", "Too generic"),
        ("proven track record", "Overused phrase"),
        ("leverage my", "Corporate jargon"),
        ("utilize my", "Just say 'use'"),
        ("synergy", "Buzzword"),
        ("seasoned", "Overused adjective"),
        ("I believe I would be", "Sounds uncertain"),
        ("extensive experience", "Too vague"),
        ("results-driven", "Empty descriptor"),
        ("team player", "Show, don't tell"),
        ("hard-working", "Show, don't tell"),
        ("—", "Replace em-dashes with commas"),
    ]
    
    for phrase, suggestion in ai_phrases:
        if phrase.lower() in clean_text.lower():
            issues.append({
                "type": "ai_phrase",
                "message": f'Found "{phrase}" - {suggestion}',
                "severity": "error"
            })
            score -= 5
    
    # Specific metrics check
    has_numbers = bool(re.search(r'\d+[KMB%]|\d+,\d+|\d+\+', clean_text))
    if has_numbers:
        issues.append({"type": "metrics", "message": "Good use of specific numbers/metrics", "severity": "pass"})
    else:
        issues.append({"type": "metrics", "message": "Add specific numbers (e.g., '16M rows', '10x faster')", "severity": "warning"})
        score -= 10
    
    # First person overuse
    i_count = len(re.findall(r'\bI\b', clean_text))
    sentences = len(re.findall(r'[.!?]', clean_text)) or 1
    i_ratio = i_count / sentences
    
    if i_ratio > 1.5:
        issues.append({"type": "tone", "message": "Too many 'I' statements - vary sentence structure", "severity": "warning"})
        score -= 5
    
    # Sentence length check
    sentences_list = re.split(r'[.!?]', clean_text)
    long_sentences = [s for s in sentences_list if len(s.split()) > 25]
    if long_sentences:
        issues.append({
            "type": "readability",
            "message": f"{len(long_sentences)} sentences are too long (>25 words)",
            "severity": "warning"
        })
        score -= len(long_sentences) * 2
    
    # Check for action verbs at start
    action_verbs = ["built", "created", "developed", "designed", "shipped", "deployed", "processed", "reduced", "improved", "automated"]
    has_action_start = any(clean_text.lower().strip().startswith(verb) for verb in action_verbs)
    if not has_action_start:
        # Check if any sentence starts with action verb
        for sentence in sentences_list:
            if any(sentence.strip().lower().startswith(verb) for verb in action_verbs):
                has_action_start = True
                break
    
    if has_action_start:
        issues.append({"type": "impact", "message": "Good - starts with action/achievement", "severity": "pass"})
    else:
        issues.append({"type": "impact", "message": "Consider starting with an achievement", "severity": "info"})
    
    # Ensure score doesn't go below 0
    score = max(0, score)
    
    # Categorize issues
    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]
    passes = [i for i in issues if i["severity"] == "pass"]
    
    return {
        "score": score,
        "grade": get_grade(score),
        "word_count": word_count,
        "issues": issues,
        "errors": errors,
        "warnings": warnings,
        "passes": passes,
        "summary": f"{len(errors)} errors, {len(warnings)} warnings, {len(passes)} passed"
    }


def get_grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def format_review_html(review: dict) -> str:
    grade_colors = {
        "A": "#10B981",  # Green
        "B": "#22C55E",  # Light green
        "C": "#F59E0B",  # Yellow
        "D": "#EF4444",  # Red
        "F": "#DC2626",  # Dark red
    }
    
    color = grade_colors.get(review["grade"], "#666")
    
    html = f"""
    <div style="background: rgba(103, 126, 234, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="background: {color}; color: white; font-size: 2rem; font-weight: bold; 
                        width: 60px; height: 60px; border-radius: 50%; display: flex; 
                        align-items: center; justify-content: center;">
                {review['grade']}
            </div>
            <div>
                <div style="font-size: 1.5rem; font-weight: bold;">{review['score']}/100</div>
                <div style="color: #888;">{review['word_count']} words • {review['summary']}</div>
            </div>
        </div>
    </div>
    """
    
    return html
