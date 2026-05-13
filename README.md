# AI-Based-Resume-Screening-Job-Matching-System

🤖 AI-Based Resume Screening & Job Matching System

An intelligent recruitment solution that automates the process of parsing resumes, extracting key skills, and matching candidates to job descriptions using Natural Language Processing (NLP).

🚀 Key Features

Resume Parsing: Automatically extracts text and structured data from uploaded resumes (PDF/DOCX).
Skill Extraction: Identification of technical and soft skills using a dedicated extraction module.
Job Matching: Algorithmic scoring to match candidate profiles with specific job requirements.
Secure Authentication: Role-based access control for Recruiters and Candidates.
Analytics Dashboard: Visual representation of candidate-job fit scores.

🛠️ Tech Stack :-

Backend: Python, Flask (via app.py)
Database: SQLite (resume_analyzer.db) with SQLAlchemy models
Frontend: HTML/CSS Templates with responsive UI
AI/NLP: Custom modules for skill extraction and profile matching

⚙️ Installation & Setup :-

Clone the Repository :-
git clone https://github.com/parmanandraj/AI-Based-Resume-Screening-Job-Matching-System.git
cd AI-Based-Resume-Screening-Job-Matching-System

Install Dependencies :-
pip install -r requirements.txt

Run the Application :-
python app.py

📝 UsageCandidates:-

Register and upload your resume to the uploads/ directory.
System: The resume_parser and skill_extractor modules will process your file.
Recruiters: View the "Matcher" results to see which candidates best fit your job openings.
