from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def calculate_job_match(resume_text, job_desc):
    if not job_desc or len(job_desc.strip()) < 10:
        return 0.0
    
    docs = [resume_text, job_desc]
    try:
        tfidf_matrix = TfidfVectorizer(stop_words='english').fit_transform(docs)
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return round(cosine_sim[0][0] * 100, 2)
    except Exception:
        return 0.0

def generate_resume_score(skills_extracted, sections_found):
    score = 0
    feedback_missing = []
    feedback_weak = []
    feedback_strong = []
    
    # Experience - 25%
    if sections_found.get('experience'):
        score += 25
        feedback_strong.append("Experience section is present")
    else:
        feedback_missing.append("Experience section")
        
    # Education - 20%
    if sections_found.get('education'):
        score += 20
        feedback_strong.append("Education section is present")
    else:
        feedback_missing.append("Education section")
        
    # Skills relevance - 40%
    skill_count = len(skills_extracted)
    if skill_count >= 5:
        score += 40
        feedback_strong.append(f"Good technical keywords ({skill_count} detected)")
    elif skill_count > 0:
        score += skill_count * 8
        feedback_weak.append("Include more technical skills / keywords")
    else:
        feedback_missing.append("Technical skills matching industry standards")
        
    # Keyword optimization & Formatting - 15%
    if sections_found.get('projects') and sections_found.get('skills'):
        score += 15
        feedback_strong.append("Clear structure with dedicated Projects/Skills sections")
    else:
        feedback_weak.append("Use standard headings like 'Projects' and 'Skills' for ATS parsers")
        
    return {
        "score": min(score, 100),
        "missing": feedback_missing,
        "weak": feedback_weak,
        "strong": feedback_strong
    }
