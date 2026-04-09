import json

# Basic skill database
SKILLS_DB = [
    "python", "java", "html", "css", "javascript",
    "react", "node", "sql", "machine learning",
    "data analysis", "django", "flask"
]

def extract_skills(text):
    found_skills = []
    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)
    return found_skills

def match_jobs(user_skills):
    with open("backend/job_data.json") as f:
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