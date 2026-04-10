from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pdfplumber
import json
import re
app = Flask(__name__)
CORS(app)

# ---------- Extract Text ----------
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

# ---------- Smart Skill Extraction ----------
import re

def extract_skills(text):
    # Comprehensive Engineering & B.Tech Skill Map
    skill_map = {
        # Software Development
        "Python": ["python", "py", "django", "flask", "fastapi", "pandas", "numpy"],
        "Java": ["java", "springboot", "hibernate", "maven", "jsp"],
        "JavaScript": ["js", "javascript", "typescript", "ts", "es6"],
        "Frontend": ["react", "angular", "vue", "nextjs", "html5", "css3", "tailwind", "sass"],
        "Backend": ["node.js", "express", "go", "golang", "php", "laravel", "ruby", "rails"],
        "Mobile": ["flutter", "react native", "android", "ios", "swift", "kotlin"],
        
        # Data Science & AI
        "Machine Learning": ["ml", "machine learning", "scikit-learn", "tensorflow", "pytorch", "keras"],
        "Data Science": ["data science", "nlp", "computer vision", "cv", "deep learning"],
        "Big Data": ["hadoop", "spark", "pyspark", "kafka", "hive"],
        "Database": ["sql", "mysql", "postgresql", "mongodb", "nosql", "redis", "oracle"],
        
        # Cloud & DevOps (The Engineering Standard)
        "DevOps": ["docker", "kubernetes", "k8s", "jenkins", "terraform", "ansible"],
        "Cloud": ["aws", "azure", "gcp", "cloud computing", "lambda", "ec2", "s3"],
        "Version Control": ["git", "github", "gitlab", "bitbucket"],
        "Cybersecurity": ["ethical hacking", "penetration testing", "firewalls", "cryptography"],

        # Core Engineering (B.Tech Specialties)
        "Mechanical": ["autocad", "solidworks", "ansys", "catia", "thermodynamics", "cad"],
        "Electronics": ["vlsi", "embedded systems", "arduino", "raspberry pi", "matlab", "verilog", "pcb design"],
        "Civil": ["staad pro", "revit", "surveying", "concrete technology", "structural analysis"],
        "IoT": ["internet of things", "sensors", "mqtt", "esp32"],
        
        # Programming Fundamentals (Great for Resume matching)
        "DSA": ["dsa", "data structures", "algorithms"],
        "OOPs": ["oops", "object oriented programming", "classes", "inheritance"],
        "Operating Systems": ["linux", "unix", "windows server", "kernel"],
        "Networking": ["tcp/ip", "dns", "http", "socket programming", "vpn"],
        
        # Management & Soft Skills
        "Agile": ["agile", "scrum", "kanban", "jira"],
        "Management": ["project management", "leadership", "resource planning", "sdlc"]
    }

    found = []
    text_lower = text.lower()

    for skill, variations in skill_map.items():
        for var in variations:
            # \b ensures we match "Java" but NOT "Javascript" or "Sajava"
            pattern = r'\b' + re.escape(var.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill)
                break # Move to next skill category once a variant is found

    return sorted(list(set(found)))

# ---------- Job Matching ----------
def match_jobs(user_skills):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "job_data.json")

    with open(file_path) as f:
        jobs = json.load(f)

    results = []

    for job in jobs:
        required = job["skills"]
        matched = list(set(user_skills) & set(required))

        match_percent = int((len(matched) / len(required)) * 100)

        results.append({
            "role": job["role"],
            "match": match_percent,
            "missing": list(set(required) - set(user_skills))
        })

    return sorted(results, key=lambda x: x["match"], reverse=True)

# ---------- Routes ----------
@app.route("/")
def home():
    return "Backend is working"

@app.route("/upload", methods=["POST"])
def upload_resume():
    try:
        file = request.files.get("resume")

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        filename = file.filename.replace(" ", "_")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        upload_folder = os.path.join(BASE_DIR, "../uploads")
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        text = extract_text_from_pdf(file_path)
        skills = extract_skills(text)
        jobs = match_jobs(skills)

        overall_score = sum(job["match"] for job in jobs) // len(jobs)

        return jsonify({
            "skills": skills,
            "jobs": jobs,
            "score": overall_score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)