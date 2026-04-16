from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import docx
import re

app = Flask(__name__)
CORS(app)

# ---------- Skill Intelligence ----------
SKILL_MAP = {
    "Python": ["python", "py", "django", "flask", "fastapi", "pandas", "numpy", "pytorch"],
    "Java": ["java", "springboot", "hibernate", "maven"],
    "C++": ["c++", "cpp", "stl", "embedded", "dsa"],
    "JavaScript": ["js", "javascript", "typescript", "react", "nextjs", "node", "express"],
    "Cloud": ["aws", "azure", "gcp", "cloud computing", "terraform"],
    "DevOps": ["docker", "kubernetes", "jenkins", "ansible", "cicd"],
    "Data Science": ["data science", "nlp", "computer vision", "statistics"],
    "Cybersecurity": ["penetration testing", "ethical hacking", "cryptography", "network security"],
    "Blockchain": ["solidity", "web3", "ethereum", "smart contracts", "rust"],
    "Databases": ["sql", "mysql", "postgresql", "mongodb", "nosql", "redis"],
    "UI/UX": ["figma", "adobe xd", "ui/ux", "wireframing", "prototyping"],
}

# ---------- CAREER DATABASE: Add more roles here! ----------
# --- MASTER CAREER DATABASE (20+ ROLES) ---
# Replace your current CAREER_DB list with this code.

CAREER_DB = [
    {
        "role": "Agentic AI Engineer",
        "salary": "₹15L - ₹55L",
        "future": "Explosive - Designing AI Agents that take actions, not just chat.",
        "work": "Building autonomous AI workflows, Model Context Protocol (MCP) servers, and RAG pipelines.",
        "required": ["Python", "Machine Learning", "Data Science", "Databases"],
        "roadmap": {
            "Python": "Python for AI Agents (DeepLearning.AI)",
            "Machine Learning": "Agentic Workflows by LangChain (YouTube)",
            "Databases": "Vector DB Mastery (Pinecone/Milvus Docs)"
        }
    },
    {
        "role": "Full Stack Engineer",
        "salary": "₹8L - ₹28L",
        "future": "Stable - High demand for versitile SaaS architects.",
        "work": "Building high-performance web apps using Next.js, TypeScript, and Prisma.",
        "required": ["JavaScript", "Databases", "Cloud", "DSA"],
        "roadmap": {
            "JavaScript": "Namaste JavaScript by Akshay Saini",
            "Databases": "SQL Mastery (CodeWithMosh)",
            "Cloud": "AWS Certified Developer - Associate"
        }
    },
    {
        "role": "Quant Researcher (HFT)",
        "salary": "₹35L - ₹95L+",
        "future": "Elite - High-frequency trading remains the most lucrative niche.",
        "work": "Developing low-latency C++ algorithms for global stock markets.",
        "required": ["C++", "Python", "Data Science", "Math"],
        "roadmap": {
            "C++": "The Cherno C++ Series (YouTube)",
            "Math": "Linear Algebra (MIT OCW) & Stochastic Calculus",
            "Data Science": "Quantitative Finance Path (Coursera)"
        }
    },
    {
        "role": "Cybersecurity Specialist",
        "salary": "₹10L - ₹35L",
        "future": "Very High - Shift toward AI-driven threat hunting.",
        "work": "Defending enterprise networks and performing Zero Trust security audits.",
        "required": ["Cybersecurity", "Networking", "Databases", "Python"],
        "roadmap": {
            "Cybersecurity": "TryHackMe (Complete Beginner Path)",
            "Networking": "CompTIA Network+ or Cisco CCNA",
            "Python": "Python for Cybersecurity (Cybrary)"
        }
    },
    {
        "role": "DevOps Architect",
        "salary": "₹12L - ₹38L",
        "future": "Critical - Infrastructure as Code (IaC) is now mandatory.",
        "work": "Automating cloud scaling with Kubernetes and Terraform.",
        "required": ["DevOps", "Cloud", "Networking", "Python"],
        "roadmap": {
            "DevOps": "TechWorld with Nana (Docker/K8s Path)",
            "Cloud": "AWS Solutions Architect Associate (SAA-C03)",
            "Networking": "Kubernetes Certified Administrator (CKA)"
        }
    },
    {
        "role": "Blockchain Developer",
        "salary": "₹12L - ₹45L",
        "future": "Growing - Focus on DeFi, Smart Contracts, and Supply Chain.",
        "work": "Developing decentralized apps (DApps) on Ethereum/Solana.",
        "required": ["Blockchain", "JavaScript", "C++", "Databases"],
        "roadmap": {
            "Blockchain": "Patrick Collins 32-hour Solidity Course",
            "JavaScript": "Web3.js Documentation & Alchemy University",
            "C++": "Smart Contract Security (Hacken Proof)"
        }
    },
    {
        "role": "Data Engineer",
        "salary": "₹10L - ₹28L",
        "future": "Essential - Scaling Big Data for AI consumption.",
        "work": "Building ETL pipelines and managing Data Lakes (Snowflake/BigQuery).",
        "required": ["Python", "Databases", "Cloud", "Java"],
        "roadmap": {
            "Databases": "Snowflake Certification Path",
            "Python": "Data Engineering Zoomcamp (DataTalks.Club)",
            "Cloud": "Google Professional Data Engineer"
        }
    },
    {
        "role": "VLSI Design Engineer",
        "salary": "₹12L - ₹35L",
        "future": "Rising - India’s push into Semiconductor Manufacturing.",
        "work": "Designing integrated circuits (ICs) and Chip-level hardware.",
        "required": ["C++", "Math", "IoT", "Networking"],
        "roadmap": {
            "C++": "Verilog & SystemVerilog for Designers",
            "IoT": "VLSI Physical Design (NPTEL - IIT Kharagpur)",
            "Math": "Digital Electronics (Morris Mano)"
        }
    },
    {
        "role": "SRE (Site Reliability Engineer)",
        "salary": "₹14L - ₹40L",
        "future": "High - Keeping global apps online at 99.9% uptime.",
        "work": "Monitoring, incident response, and performance tuning.",
        "required": ["Cloud", "DevOps", "Python", "Networking"],
        "roadmap": {
            "Cloud": "Microsoft Certified: Azure Administrator",
            "DevOps": "SRE Fundamentals (Google Cloud Skills)",
            "Python": "Linux System Administration (YouTube)"
        }
    },
    {
        "role": "UI/UX Product Engineer",
        "salary": "₹7L - ₹22L",
        "future": "High - User experience is the #1 market differentiator.",
        "work": "Designing user flows in Figma and building them in React.",
        "required": ["UI/UX", "JavaScript", "Frontend", "Cloud"],
        "roadmap": {
            "UI/UX": "Google UX Design Professional Cert",
            "JavaScript": "Three.js Journey (for 3D Interfaces)",
            "Frontend": "Tailwind CSS Documentation"
        }
    },
    {
        "role": "IoT Solution Architect",
        "salary": "₹8L - ₹25L",
        "future": "High - Smart Cities and Industrial IoT growth.",
        "work": "Interconnecting sensors and actuators with Cloud dashboards.",
        "required": ["IoT", "C++", "Cloud", "Networking"],
        "roadmap": {
            "IoT": "Arduino & Raspberry Pi Masterclass",
            "C++": "MQTT Protocol Fundamentals",
            "Networking": "Certified IoT Professional (IIC)"
        }
    },
    {
        "role": "AR/VR Developer",
        "salary": "₹12L - ₹32L",
        "future": "Emerging - Spatial Computing (Apple Vision Pro/Meta Quest).",
        "work": "Developing 3D immersive environments and game physics.",
        "required": ["C++", "Math", "UI/UX", "JavaScript"],
        "roadmap": {
            "C++": "Unity (C#) or Unreal Engine (C++) Path",
            "Math": "3D Math for Games (Essential Graphics)",
            "JavaScript": "React-Three-Fiber (R3F) Mastery"
        }
    },
    {
        "role": "Product Manager (Tech)",
        "salary": "₹15L - ₹35L",
        "future": "Strategic - Bridging the gap between code and customers.",
        "work": "Managing product lifecycle and engineering sprint planning.",
        "required": ["Management", "Data Science", "UI/UX", "Cloud"],
        "roadmap": {
            "Management": "Pragmatic Institute PM Cert",
            "Data Science": "Product Analytics (Mixpanel/Amplitude)",
            "UI/UX": "User Psychology (Coursera)"
        }
    },
    {
        "role": "Mobile App Developer",
        "salary": "₹8L - ₹22L",
        "future": "Stable - Constant need for high-speed iOS/Android apps.",
        "work": "Building native/cross-platform apps using Flutter or React Native.",
        "required": ["JavaScript", "UI/UX", "Cloud", "DSA"],
        "roadmap": {
            "JavaScript": "React Native - The Practical Guide",
            "UI/UX": "Material Design vs. Apple HIG",
            "Cloud": "Firebase for Mobile (YouTube)"
        }
    },
    {
        "role": "Renewable Energy Engineer",
        "salary": "₹6L - ₹18L",
        "future": "Sustainable - Transitioning the world to Green Energy.",
        "work": "Designing solar/wind grids and energy storage systems.",
        "required": ["Math", "Networking", "IoT", "Cloud"],
        "roadmap": {
            "Math": "Solar PV System Design (NPTEL)",
            "Networking": "Smart Grid Communication Protocols",
            "IoT": "Energy Monitoring Systems (SCADA)"
        }
    },
    {
        "role": "Cloud Security Architect",
        "salary": "₹18L - ₹45L",
        "future": "Very High - Preventing massive data leaks in the cloud.",
        "work": "Designing Secure Identity Management (IAM) and Cloud Firewalls.",
        "required": ["Cloud", "Cybersecurity", "Networking", "DevOps"],
        "roadmap": {
            "Cloud": "AWS Certified Security Specialty",
            "Cybersecurity": "Certified Cloud Security Professional (CCSP)",
            "Networking": "Palo Alto Networks Cloud Security"
        }
    },
    {
        "role": "Embedded Systems Engineer",
        "salary": "₹8L - ₹24L",
        "future": "High - Essential for the EV and Robotics sectors.",
        "work": "Programming microcontrollers for automobiles and medical devices.",
        "required": ["C++", "IoT", "Networking", "Math"],
        "roadmap": {
            "C++": "Bare Metal Programming in C/C++",
            "IoT": "ARM Architecture (EdX)",
            "Networking": "CAN Bus & Automotive Networking"
        }
    },
    {
        "role": "Data Scientist",
        "salary": "₹10L - ₹30L",
        "future": "High - Turning raw data into business strategy.",
        "work": "Statistical modeling, predictive analytics, and executive dashboards.",
        "required": ["Python", "Data Science", "Math", "Databases"],
        "roadmap": {
            "Python": "Python for Data Science (IBM)",
            "Data Science": "Tableau & PowerBI Mastery",
            "Math": "Statistics (Khan Academy)"
        }
    },
    {
        "role": "Cloud Consultant",
        "salary": "₹9L - ₹24L",
        "future": "Stable - Migrating legacy businesses to the modern cloud.",
        "work": "Advising businesses on digital transformation and cost optimization.",
        "required": ["Cloud", "Management", "Networking", "Databases"],
        "roadmap": {
            "Cloud": "Azure Fundamentals (AZ-900)",
            "Management": "Digital Transformation (Coursera)",
            "Networking": "Google Associate Cloud Engineer"
        }
    },
    {
        "role": "Software Project Manager",
        "salary": "₹12L - ₹32L",
        "future": "High - Managing complex engineering deliverables.",
        "work": "Ensuring code quality, deadlines, and client communication.",
        "required": ["Management", "JavaScript", "DevOps", "Cloud"],
        "roadmap": {
            "Management": "PMP Certification (PMI)",
            "JavaScript": "Agile Software Development (Coursera)",
            "DevOps": "Jira & Confluence Mastery"
        }
    },
    # Continue pasting these inside the CAREER_DB list in app.py

    {
        "role": "Robotics & Automation Engineer",
        "salary": "₹8L - ₹26L",
        "future": "High - Essential for Industry 4.0 and autonomous warehouse logistics.",
        "work": "Integrating computer vision with mechanical actuators for smart automation.",
        "required": ["C++", "Python", "IoT", "Math"],
        "roadmap": {
            "Math": "Control Systems & Robotics (NPTEL - IIT Bombay)",
            "Python": "ROS (Robot Operating System) Fundamentals",
            "C++": "Computer Vision with OpenCV (Udemy)"
        }
    },
    {
        "role": "Bioinformatics Scientist",
        "salary": "₹12L - ₹30L",
        "future": "Explosive - Merging DNA sequencing with AI for personalized medicine.",
        "work": "Using computational tools to analyze biological data and accelerate drug discovery.",
        "required": ["Python", "Data Science", "Databases", "Math"],
        "roadmap": {
            "Data Science": "Genomic Data Science Specialization (Coursera)",
            "Python": "BioPython Mastery & R Programming",
            "Databases": "NCBI Database Management & SQL"
        }
    },
    {
        "role": "Electric Vehicle (EV) Powertrain Engineer",
        "salary": "₹9L - ₹24L",
        "future": "Very High - The global shift to electric mobility is unstoppable.",
        "work": "Designing Battery Management Systems (BMS) and motor control logic.",
        "required": ["IoT", "Math", "C++", "Networking"],
        "roadmap": {
            "IoT": "EV Technology & Design (NPTEL)",
            "C++": "Model-Based Design with MATLAB/Simulink",
            "Math": "Power Electronics for EV (Coursera)"
        }
    },
    {
        "role": "FinTech Backend Developer",
        "salary": "₹12L - ₹35L",
        "future": "Stable - Powering the next generation of UPI, Neo-banks, and Digital Lending.",
        "work": "Developing high-concurrency payment gateways and ledger systems.",
        "required": ["Java", "Databases", "Cloud", "Cybersecurity"],
        "roadmap": {
            "Java": "Spring Boot Microservices Architecture",
            "Databases": "Distributed Systems & Transactional Integrity",
            "Cybersecurity": "PCI-DSS Compliance Standards"
        }
    },
    {
        "role": "Industrial UI/UX Designer (HMI)",
        "salary": "₹8L - ₹18L",
        "future": "Rising - Designing interfaces for complex factory machines and cockpits.",
        "work": "Creating Human-Machine Interfaces (HMI) that are functional and error-proof.",
        "required": ["UI/UX", "IoT", "JavaScript", "Math"],
        "roadmap": {
            "UI/UX": "HMI Design for Industry (Interaction Design Foundation)",
            "JavaScript": "SCADA/HMI Visualization Tools",
            "IoT": "Industrial Design Thinking"
        }
    },
]

def parse_file(file):
    name = file.filename.lower()
    text = ""
    try:
        if name.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                text = "\n".join([p.extract_text() or "" for p in pdf.pages])
        elif name.endswith(".docx"):
            doc = docx.Document(file)
            text = "\n".join([p.text for p in doc.paragraphs])
        return text.lower()
    except Exception: return ""

@app.route("/analyze", methods=["POST"])
def analyze():
    text = ""
    if 'resume' in request.files:
        text = parse_file(request.files['resume'])
    else:
        text = request.json.get('manual_text', '').lower()

    found = []
    for skill, variants in SKILL_MAP.items():
        for v in variants:
            if re.search(r'\b' + re.escape(v) + r'\b', text):
                found.append(skill)
                break
    
    results = []
    for job in CAREER_DB:
        matched = list(set(found) & set(job["required"]))
        # Logic: Only show jobs that have at least one skill match to keep it relevant
        if matched:
            score = int((len(matched) / len(job["required"])) * 100)
            missing = list(set(job["required"]) - set(found))
            results.append({
                **job,
                "match": score,
                "missing": missing,
                "guides": {s: job["roadmap"].get(s, "Master on Coursera/NPTEL") for s in missing}
            })
        
    return jsonify({
        "user_skills": found,
        "results": sorted(results, key=lambda x: x["match"], reverse=True)
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)