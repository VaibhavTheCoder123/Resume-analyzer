from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pdfplumber
import json

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
def extract_skills(text):
    skill_map = {
        "python": ["python"],
        "java": ["java"],
        "html": ["html"],
        "css": ["css"],
        "javascript": ["js", "javascript"],
        "react": ["react"],
        "node": ["node", "nodejs"],
        "sql": ["sql", "mysql"],
        "machine learning": ["ml", "machine learning"],
        "data analysis": ["data analysis", "pandas", "numpy"],
        "django": ["django"],
        "flask": ["flask"]
    }

    found = []

    for skill, variations in skill_map.items():
        for word in variations:
            if word in text:
                found.append(skill)
                break

    return list(set(found))

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