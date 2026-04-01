import spacy
import nltk
from nltk.corpus import stopwords
import re
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Try to load spacy model, fallback if not downloaded yet
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load('en_core_web_sm')

try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english'))

SKILLS_DB = [
    'python', 'java', 'sql', 'c++', 'javascript', 'html', 'css', 'react', 'node', 'nodejs',
    'machine learning', 'deep learning', 'nlp', 'data analysis', 'flask', 'django',
    'fastapi', 'aws', 'docker', 'kubernetes', 'git', 'agile', 'scrum', 'leadership',
    'communication', 'teamwork', 'problem solving', 'c', 'c#', 'php', 'ruby', 'go',
    'rust', 'spark', 'hadoop', 'mongodb', 'postgresql', 'mysql', 'sqlite', 'redis',
    'elasticsearch', 'tensorflow', 'keras', 'pytorch', 'scikit-learn', 'pandas',
    'numpy', 'matplotlib', 'seaborn', 'tableau', 'powerbi', 'excel', 'word', 'powerpoint',
    'bootstrap', 'jwt', 'rest api', 'graphql', 'linux', 'bash', 'shell'
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    tokens = [word for word in text.split() if word not in stop_words]
    return " ".join(tokens)

def extract_skills(text):
    text = text.lower()
    extracted = set()
    
    # Simple match against DB
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            extracted.add(skill)
            
    return list(extracted)

def check_sections(text):
    sections_found = {
        'education': False,
        'experience': False,
        'projects': False,
        'skills': False
    }
    
    text = text.lower()
    if re.search(r'\b(education|academic|university|college|degree)\b', text):
        sections_found['education'] = True
    if re.search(r'\b(experience|employment|work history|career)\b', text):
        sections_found['experience'] = True
    if re.search(r'\b(projects|portfolio|personal projects)\b', text):
        sections_found['projects'] = True
    if re.search(r'\b(skills|technologies|technical skills|core competencies)\b', text):
        sections_found['skills'] = True
        
    return sections_found
