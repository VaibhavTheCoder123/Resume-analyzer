import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Upload, Edit3, Briefcase, TrendingUp, DollarSign, 
  BrainCircuit, GraduationCap, CheckCircle, Search, Rocket, Zap, Cpu
} from "lucide-react";
import confetti from "canvas-confetti";

const App = () => {
  const [mode, setMode] = useState("upload");
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const analyzeProfile = async () => {
    setLoading(true);
    const formData = new FormData();
    if (mode === "upload" && file) formData.append("resume", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        body: mode === "upload" ? formData : JSON.stringify({ manual_text: input }),
        headers: mode === "manual" ? { "Content-Type": "application/json" } : {},
      });
      const data = await response.json();
      setResults(data);
      if (data.results.length > 0) confetti({ particleCount: 150, spread: 70 });
    } catch (error) {
      alert("Backend Not Responding.");
    } finally {
      setLoading(false);
    }
  };

  const filteredResults = results?.results.filter(job => 
    job.role.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen relative p-4 md:p-12 app-shell">
      <div className="aurora-bg" />
      
      <header className="max-w-7xl mx-auto flex justify-between items-center mb-16 relative z-10">
        <div className="flex items-center gap-3">
          <BrainCircuit className="text-purple-500" size={32} />
          <h1 className="brand-text">Vairo's <span className="text-purple-500">AI</span></h1>
        </div>
        <div className="version-badge">Career Architecture System</div>
      </header>

      <main className="max-w-5xl mx-auto relative z-10">
        {/* CENTERED HERO SECTION */}
        <div className="hero-container text-center mb-12">
          <motion.h2 
            initial={{ opacity: 0, y: -20 }} 
            animate={{ opacity: 1, y: 0 }} 
            className="hero-title"
          >
            Bridge the <span className="text-gradient">Skill Gap.</span>
          </motion.h2>
        </div>

        {/* --- Intelligence Feature Hub --- */}
        <div className="feature-hub glass-card">
          <div className="feature-item">
            <Cpu size={20} className="text-purple-400" />
            <div className="feature-content">
              <h4>Skill Extraction</h4>
              <p>Neural mapping to 2026 standards.</p>
            </div>
          </div>
          <div className="feature-item divider">
            <TrendingUp size={20} className="text-blue-400" />
            <div className="feature-content">
              <h4>Market Insights</h4>
              <p>Live salary metrics for 25+ paths.</p>
            </div>
          </div>
          <div className="feature-item">
            <GraduationCap size={20} className="text-green-400" />
            <div className="feature-content">
              <h4>Roadmap Linker</h4>
              <p>Verified certification paths.</p>
            </div>
          </div>
        </div>

        {/* Input Card */}
        <div className="glass-card main-input-card p-8 mb-16">
          <div className="mode-toggle-wrapper">
            <button onClick={() => setMode("upload")} className={`mode-btn ${mode === 'upload' ? 'active' : ''}`}><Upload size={16} /> Upload Profile</button>
            <button onClick={() => setMode("manual")} className={`mode-btn ${mode === 'manual' ? 'active' : ''}`}><Edit3 size={16} /> Manual Entry</button>
          </div>

          <div className="space-y-6">
            {mode === "upload" ? (
              <div className="upload-dropzone">
                <input type="file" onChange={(e) => setFile(e.target.files[0])} className="hidden-input" />
                <Rocket className="rocket-icon" size={48} />
                <p className="upload-text">{file ? file.name : "Select Resume (PDF/Docx)"}</p>
              </div>
            ) : (
              <textarea 
                onChange={(e) => setInput(e.target.value)}
                className="manual-textarea"
                placeholder="Paste your skills or professional bio..."
              />
            )}
            <button onClick={analyzeProfile} disabled={loading} className="analyze-btn">
              {loading ? "Decrypting DNA..." : "Start Analysis"}
            </button>
          </div>
        </div>

        {/* Results Search */}
        {results && (
          <div className="search-bar-wrapper mb-8">
            <Search className="search-icon" size={20} />
            <input 
              type="text" 
              placeholder="Search careers in results..." 
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
          </div>
        )}

        <AnimatePresence>
          <div className="results-grid">
            {filteredResults?.map((job, idx) => (
              <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="glass-card result-card relative" key={idx}>
                <div className="salary-badge">
                  <DollarSign size={12} /> {job.salary}
                </div>
                <div className="result-header">
                  <div>
                    <h3 className="role-title">{job.role}</h3>
                    <div className="role-metrics">
                      <span className="metric future"><Zap size={14} className="trending-icon" /> {job.future}</span>
                    </div>
                  </div>
                  <div className="match-score">{job.match}%</div>
                </div>
                <p className="work-desc">{job.work}</p>
                <div className="roadmap-box">
                  <h4 className="roadmap-title"><GraduationCap size={16}/> Skill Roadmap</h4>
                  {job.missing.map(m => (
                    <div key={m} className="roadmap-item">
                      <div>
                        <p className="skill-name">{m}</p>
                        <p className="guide-text">{job.guides[m]}</p>
                      </div>
                      <a href={`https://www.google.com/search?q=${m}+certification+2026`} target="_blank" className="cert-search"><Search size={14}/></a>
                    </div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </AnimatePresence>
      </main>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&display=swap');
        body { background: #050505; color: white; font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; }
        .aurora-bg { position: fixed; inset: 0; background: radial-gradient(circle at 0% 0%, #aa3bff22 0%, transparent 40%); z-index: -1; }
        .brand-text { font-size: 1.5rem; font-weight: 800; letter-spacing: -1px; }
        .version-badge { font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 2px; font-weight: 800; }
        
        .hero-title { 
          font-size: 4rem; 
          font-weight: 800; 
          letter-spacing: -2px; 
          margin: 0; 
          text-align: center;
        }
        .hero-container {
          margin-bottom: 50px; /* Space below the centered title */
        }
        .text-gradient { background: linear-gradient(90deg, #aa3bff, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        .feature-hub {
          display: flex;
          justify-content: space-around;
          align-items: center;
          padding: 20px;
          margin: 0 auto 30px;
          max-width: 800px;
        }
        .feature-item { display: flex; align-items: center; gap: 12px; }
        .divider { border-left: 1px solid rgba(255,255,255,0.1); border-right: 1px solid rgba(255,255,255,0.1); padding: 0 30px; }
        .feature-content h4 { font-size: 0.8rem; font-weight: 800; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
        .feature-content p { font-size: 0.7rem; color: #666; margin: 2px 0 0; }

        .glass-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 28px; backdrop-filter: blur(20px); }
        .main-input-card { max-width: 700px; margin: 0 auto 4rem; padding: 40px; }
        .mode-toggle-wrapper { display: flex; background: rgba(255,255,255,0.05); padding: 5px; border-radius: 15px; width: fit-content; margin: 0 auto 2rem; }
        .mode-btn { border: none; background: none; color: #777; padding: 10px 20px; border-radius: 12px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 8px; }
        .mode-btn.active { background: white; color: black; }
        .upload-dropzone { border: 2px dashed rgba(255,255,255,0.1); border-radius: 20px; padding: 50px 20px; text-align: center; position: relative; cursor: pointer; }
        .hidden-input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
        .rocket-icon { color: #aa3bff; margin: 0 auto 1rem; }
        .analyze-btn { width: 100%; background: #aa3bff; border: none; padding: 20px; border-radius: 15px; color: white; font-weight: 800; font-size: 1.1rem; cursor: pointer; box-shadow: 0 10px 30px rgba(170, 59, 255, 0.2); transition: 0.3s; }
        .analyze-btn:hover { transform: translateY(-3px); background: #9626e5; }
        .search-bar-wrapper { max-width: 700px; margin: 0 auto; position: relative; }
        .search-icon { position: absolute; left: 24px; top: 50%; transform: translateY(-50%); color: #555; }
        .search-input { width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 18px 18px 18px 60px; border-radius: 100px; color: white; outline: none; box-sizing: border-box; }
        
        .results-grid { display: grid; grid-template-columns: 1fr; gap: 2rem; margin-top: 2rem; padding-bottom: 5rem; }
        .result-card { padding: 40px; position: relative; }
        .salary-badge { position: absolute; top: 20px; right: 20px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); color: #10b981; padding: 6px 14px; border-radius: 100px; font-size: 11px; font-weight: 800; display: flex; align-items: center; gap: 6px; }
        .result-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; }
        .role-title { font-size: 1.8rem; font-weight: 800; margin: 0; max-width: 70%; }
        .role-metrics { display: flex; gap: 1rem; margin-top: 12px; }
        .metric { font-size: 10px; font-weight: 800; text-transform: uppercase; padding: 4px 10px; border-radius: 8px; display: flex; align-items: center; gap: 6px; }
        .future { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
        .trending-icon { animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
        .match-score { font-size: 2.5rem; font-weight: 900; color: #aa3bff; }
        .work-desc { color: #888; line-height: 1.6; margin-bottom: 2rem; }
        .roadmap-box { background: rgba(0,0,0,0.2); padding: 25px; border-radius: 24px; border: 1px solid rgba(255,255,255,0.05); }
        .roadmap-title { font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; color: #555; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 8px; }
        .roadmap-item { display: flex; justify-content: space-between; align-items: center; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 1rem; }
        .roadmap-item:last-child { border: none; margin: 0; padding: 0; }
        .skill-name { font-weight: 700; margin: 0; }
        .guide-text { font-size: 12px; color: #666; margin-top: 2px; }
        .cert-search { padding: 10px; background: rgba(255,255,255,0.05); border-radius: 10px; color: white; transition: 0.3s; }
        .cert-search:hover { background: #aa3bff; }
        .manual-textarea { width: 100%; height: 150px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 20px; color: white; outline: none; resize: none; box-sizing: border-box; font-size: 16px; }
      `}</style>
    </div>
  );
};

export default App;