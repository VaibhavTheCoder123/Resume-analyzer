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

if __name__ == "__main__":
    sample_text = "I have experience with python, django, and machine learning."
    skills = extract_skills(sample_text)
    print("Extracted Skills:", skills)

    job_matches = match_jobs(skills)
    print("Job Matches:", job_matches)
    results = match_jobs(skills)
    for result in results:
        print(f"Role: {result['role']}, Match: {result['match']}%, Missing Skills: {', '.join(result['missing'])}")
        if result['match'] >= 50:
            print("You are a good fit for this role!")
        else:
            print("You may want to improve your skills for this role.")
    suggestions = []
    for result in results:
        if result['match'] < 50:
            suggestions.extend(result['missing'])

    print("Suggestions for Improvement:", suggestions)
    