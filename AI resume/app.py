from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import os
import uuid
from config import Config
from models import db, Resume, User
from auth.routes import auth_bp
from security.middleware import token_required, admin_required
from resume_parser.parser import parse_resume
from skill_extractor.extractor import extract_skills, check_sections, clean_text
from matcher.scorer import calculate_job_match, generate_resume_score
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_app(app)

# Initialize Security
csrf = CSRFProtect(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return redirect(url_for('auth_bp.login_page'))

@app.route('/dashboard')
@token_required
def dashboard(current_user, user_role):
    resumes = Resume.query.filter_by(user_id=current_user).order_by(Resume.upload_date.desc()).all()
    user = User.query.get(current_user)
    return render_template('dashboard.html', resumes=resumes, username=user.username, role=user_role)

@app.route('/upload', methods=['GET', 'POST'])
@token_required
def upload(current_user, user_role):
    if request.method == 'GET':
        return render_template('upload.html')
        
    if 'resume' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
        
    file = request.files['resume']
    job_desc = request.form.get('job_description', '')
    
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
        
    if file and allowed_file(file.filename):
        random_id = str(uuid.uuid4())
        ext = file.filename.rsplit('.', 1)[1].lower()
        secure_name = f"{random_id}.{ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_name)
        file.save(file_path)
        
        raw_text = parse_resume(file_path)
        if not raw_text:
            flash('Failed to extract text from file.', 'danger')
            return redirect(request.url)
            
        extracted_skills = extract_skills(raw_text)
        sections = check_sections(raw_text)
        
        match_score = calculate_job_match(raw_text, job_desc)
        eval_results = generate_resume_score(extracted_skills, sections)
        
        new_resume = Resume(
            user_id=current_user,
            filename=file.filename,
            score=eval_results['score'],
            feedback_missing=json.dumps(eval_results['missing']),
            feedback_weak=json.dumps(eval_results['weak']),
            feedback_strong=json.dumps(eval_results['strong']),
            extracted_skills=','.join(extracted_skills),
            job_match_score=match_score
        )
        db.session.add(new_resume)
        db.session.commit()
        
        logging.info(f"User {current_user} uploaded resume {new_resume.id}")
        flash('Resume successfully analyzed', 'success')
        return redirect(url_for('analyze', resume_id=new_resume.id))
        
    flash('Invalid file type. Only PDF and DOCX are allowed.', 'danger')
    return redirect(request.url)

@app.route('/analyze/<int:resume_id>')
@token_required
def analyze(current_user, user_role, resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=current_user).first()
    if not resume:
        flash('Resume not found or unauthorized.', 'danger')
        return redirect(url_for('dashboard'))
        
    missing = json.loads(resume.feedback_missing) if resume.feedback_missing else []
    weak = json.loads(resume.feedback_weak) if resume.feedback_weak else []
    strong = json.loads(resume.feedback_strong) if resume.feedback_strong else []
    skills_list = resume.extracted_skills.split(',') if resume.extracted_skills else []
    
    return render_template('analyze.html', 
                            resume=resume, 
                            missing=missing, 
                            weak=weak, 
                            strong=strong,
                            skills_list=skills_list)

@app.route('/admin')
@token_required
@admin_required
def admin_panel(current_user, user_role):
    users_count = User.query.count()
    resumes_count = Resume.query.count()
    users = User.query.all()
    resumes = Resume.query.order_by(Resume.upload_date.desc()).limit(10).all()
    
    return render_template('admin.html', u_count=users_count, r_count=resumes_count, users=users, recent_resumes=resumes)

with app.app_context():
    db.create_all()
    from auth.routes import bcrypt
    if not User.query.filter_by(username='admin').first():
        hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(username='admin', email='admin@resume.com', password_hash=hashed_pw, role='admin')
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
