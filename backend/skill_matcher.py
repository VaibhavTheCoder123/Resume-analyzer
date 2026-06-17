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
    additional_suggestions = set(suggestions) - set(skills)
    print("Additional Suggestions for Improvement:", additional_suggestions)for result in results:    print(f"Role: {result['role']}, Match: {result['match']}%, Missing Skills: {', '.join(result['missing'])}")
    if result['match'] >= 50:
        print("You are a good fit for this role!")
    else:        print("You may want to improve your skills for this role.")
    additional_suggestions = set(suggestions) - set(skills)
    print("Additional Suggestions for Improvement:", additional_suggestions)
    Webdev_suggestions = [s for s in additional_suggestions if s in ["html", "css", "javascript", "react", "node"]]
    print("Web Development Suggestions:", Webdev_suggestions)
    Data_suggestions = [s for s in additional_suggestions if s in ["sql", "machine learning", "data analysis"]]
    print("Data Science Suggestions:", Data_suggestions)
    backend_suggestions = [s for s in additional_suggestions if s in ["python", "django", "flask"]]
    print("Backend Development Suggestions:", backend_suggestions)
    frontend_suggestions = [s for s in additional_suggestions if s in ["html", "css", "javascript", "react"]]
    print("Frontend Development Suggestions:", frontend_suggestions)
    cloud_suggestions = [s for s in additional_suggestions if s in ["aws", "azure", "gcp"]]
    print("Cloud Computing Suggestions:", cloud_suggestions)
    cyber_suggestions = [s for s in additional_suggestions if s in ["network security", "penetration testing"]]
    print("Cybersecurity Suggestions:", cyber_suggestions)
    bigdata_suggestions = [s for s in additional_suggestions if s in ["hadoop", "spark"]]
    print("Big Data Suggestions:", bigdata_suggestions)
    blockchain_suggestions = [s for s in additional_suggestions if s in ["solidity", "ethereum"]]
    print("Blockchain Suggestions:", blockchain_suggestions)
    devops_suggestions = [s for s in additional_suggestions if s in ["docker", "kubernetes"]]
    print("DevOps Suggestions:", devops_suggestions)
    devsecops_suggestions = [s for s in additional_suggestions if s in ["security automation", "compliance"]]
    print("DevSecOps Suggestions:", devsecops_suggestions)
    ai_suggestions = [s for s in additional_suggestions if s in ["deep learning", "natural language processing"]]
    print("AI Suggestions:", ai_suggestions)
    dev_suggestions = [s for s in additional_suggestions if s in ["git", "ci/cd"]]
    print("General Development Suggestions:", dev_suggestions)
    print("Overall Suggestions for Improvement:", additional_suggestions)
