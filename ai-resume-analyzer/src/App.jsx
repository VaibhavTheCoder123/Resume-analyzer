import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Upload, Cpu, Zap, Target, AlertCircle, 
  FileText, ChevronRight, LayoutGrid, Award 
} from "lucide-react";
import confetti from "canvas-confetti";

const App = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
      
      // Professional success celebration for high matches
      if (data.score > 40) {
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#aa3bff', '#60a5fa', '#ffffff']
        });
      }
    } catch (err) {
      console.error("Backend connection failed.");
      alert("Check if Flask is running on port 5000!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-wrapper">
      {/* Aurora Background Effects */}
      <div className="bg-glow top-left"></div>
      <div className="bg-glow bottom-right"></div>

      <div className="content-container">
        {/* Glassmorphism Header */}
        <motion.nav 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="glass-nav"
        >
          <div className="logo">
            <Cpu size={22} className="icon-pulse" />
            <span>ENGINEER<span className="text-gradient">SCAN</span></span>
          </div>
          <div className="nav-status">
            <span className="status-dot"></span> AI Engine Active
          </div>
        </motion.nav>

        {/* Hero Section */}
        <header className="hero-section">
          <motion.h1 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="hero-title"
          >
            Precision <span className="text-gradient">Resume</span> Analysis
          </motion.h1>
          <p className="hero-subtitle">B.Tech Industry Alignment Engine v2.0</p>
        </header>

        {/* Main Bento Grid */}
        <section className="bento-grid">
          {/* Upload Card */}
          <motion.div 
            className="bento-card upload-card"
            whileHover={{ boxShadow: "0 0 30px rgba(170, 59, 255, 0.2)" }}
          >
            <div className="card-label"><Upload size={14} /> Source Upload</div>
            <div className="upload-area">
              <input 
                type="file" 
                accept=".pdf" 
                onChange={(e) => setFile(e.target.files[0])} 
              />
              <motion.div 
                animate={file ? { scale: [1, 1.1, 1] } : {}}
                className="icon-box"
              >
                <FileText size={40} color={file ? "var(--accent)" : "#4b5563"} />
              </motion.div>
              <h3>{file ? file.name : "Drag & Drop Resume"}</h3>
              <p>Professional PDF profiles only</p>
            </div>
            
            {file && (
              <motion.button 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleUpload}
                disabled={loading}
                className="action-btn"
              >
                {loading ? "Analyzing Engineering DNA..." : "Start Analysis"}
              </motion.button>
            )}
          </motion.div>

          {/* System Metrics Card */}
          <div className="bento-card metrics-card">
            <div className="card-label"><Target size={14} /> Core Metrics</div>
            <div className="metric-row">
              <span>Match Precision</span>
              <span className="val">99.2%</span>
            </div>
            <div className="metric-row">
              <span>B.Tech Fields</span>
              <span className="val">12+</span>
            </div>
            <div className="visual-loader">
              <motion.div 
                className="loader-fill"
                animate={{ width: loading ? "100%" : "30%" }}
                transition={{ duration: 2, repeat: loading ? Infinity : 0 }}
              />
            </div>
            <p className="metric-footer">Neural Network: Optimized</p>
          </div>
        </section>

        {/* Results Display */}
        <AnimatePresence>
          {result && (
            <motion.div 
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="results-container"
            >
              <div className="results-header">
                <h2><Zap size={20} color="var(--accent)" /> Analysis Results</h2>
                <div className="overall-score">
                  Overall Alignment: <span className="text-gradient">{result.score}%</span>
                </div>
              </div>

              <div className="results-grid">
                {/* Skills Section */}
                <div className="bento-card skills-box">
                  <div className="card-label"><LayoutGrid size={14} /> Identified Engineering Skills</div>
                  <div className="skills-flex">
                    {result.skills.map((skill, i) => (
                      <motion.span 
                        key={i}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: i * 0.05 }}
                        className="skill-pill"
                      >
                        {skill}
                      </motion.span>
                    ))}
                  </div>
                </div>

                {/* Job Matches Section */}
                <div className="job-matches">
                  {result.jobs.map((job, i) => (
                    <motion.div 
                      key={i}
                      whileHover={{ x: 8, background: "rgba(255,255,255,0.04)" }}
                      className="job-card"
                    >
                      <div className="job-main">
                        <h4>{job.role}</h4>
                        <div className="missing-list">
                          {job.missing.length > 0 ? (
                            job.missing.map(m => <span key={m} className="m-item"><AlertCircle size={10}/> {m}</span>)
                          ) : (
                            <span className="perfect-match"><Award size={12}/> Best Match</span>
                          )}
                        </div>
                      </div>
                      <div className="score-box">
                        <div className="score-num">{job.match}%</div>
                        <ChevronRight size={16} color="#4b5563" />
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <style jsx>{`
        :root {
          --accent: #aa3bff;
          --accent-glow: rgba(170, 59, 255, 0.3);
          --bg-dark: #08070b;
          --glass: rgba(255, 255, 255, 0.03);
          --border: rgba(255, 255, 255, 0.08);
        }

        .main-wrapper {
          min-height: 100vh;
          background: var(--bg-dark);
          color: #f3f4f6;
          font-family: 'Inter', sans-serif;
          position: relative;
          overflow-x: hidden;
        }

        .content-container {
          max-width: 1100px;
          margin: 0 auto;
          padding: 20px;
          position: relative;
          z-index: 2;
        }

        /* Animated Backgrounds */
        .bg-glow {
          position: fixed;
          width: 50vw;
          height: 50vw;
          filter: blur(120px);
          opacity: 0.1;
          pointer-events: none;
          z-index: 1;
        }
        .top-left { top: -10%; left: -10%; background: var(--accent); animation: float 15s infinite alternate; }
        .bottom-right { bottom: -10%; right: -10%; background: #3b82f6; animation: float 20s infinite alternate-reverse; }

        @keyframes float {
          from { transform: translate(0,0); }
          to { transform: translate(10%, 5%); }
        }

        .text-gradient {
          background: linear-gradient(90deg, #aa3bff, #60a5fa);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        /* Header */
        .glass-nav {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px 24px;
          background: var(--glass);
          backdrop-filter: blur(12px);
          border: 1px solid var(--border);
          border-radius: 100px;
          margin-top: 20px;
        }
        .logo { display: flex; align-items: center; gap: 8px; font-weight: 800; letter-spacing: 1px; }
        .status-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block; margin-right: 6px; box-shadow: 0 0 10px #10b981; }

        /* Hero */
        .hero-section { text-align: center; padding: 60px 0; }
        .hero-title { font-size: 3.5rem; font-weight: 900; margin: 0; letter-spacing: -2px; }
        .hero-subtitle { color: #9ca3af; margin-top: 10px; font-size: 1.1rem; }

        /* Bento Grid */
        .bento-grid { display: grid; grid-template-columns: 1.8fr 1fr; gap: 20px; margin-bottom: 30px; }
        .bento-card {
          background: var(--glass);
          border: 1px solid var(--border);
          border-radius: 24px;
          padding: 24px;
          position: relative;
        }
        .card-label { 
          font-size: 0.7rem; 
          text-transform: uppercase; 
          color: #6b7280; 
          letter-spacing: 1.5px; 
          margin-bottom: 20px;
          display: flex;
          align-items: center;
          gap: 6px;
        }

        /* Upload Area */
        .upload-area {
          border: 2px dashed rgba(170, 59, 255, 0.2);
          border-radius: 20px;
          padding: 40px;
          text-align: center;
          position: relative;
          transition: 0.3s;
        }
        .upload-area input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
        .icon-box { margin-bottom: 15px; }
        .action-btn {
          width: 100%;
          margin-top: 20px;
          padding: 14px;
          border-radius: 12px;
          border: none;
          background: linear-gradient(135deg, #aa3bff, #7c3aed);
          color: white;
          font-weight: 700;
          cursor: pointer;
          box-shadow: 0 10px 20px rgba(124, 58, 237, 0.3);
        }

        /* Metrics Card */
        .metric-row { display: flex; justify-content: space-between; margin-bottom: 15px; font-weight: 600; }
        .val { color: var(--accent); }
        .visual-loader { height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px; overflow: hidden; margin: 20px 0; }
        .loader-fill { height: 100%; background: var(--accent); width: 30%; }
        .metric-footer { font-size: 0.7rem; color: #4b5563; text-align: center; }

        /* Results */
        .results-container { margin-top: 40px; }
        .results-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 15px; }
        .results-grid { display: grid; grid-template-columns: 1fr 1.2fr; gap: 20px; }
        
        .skills-flex { display: flex; flex-wrap: wrap; gap: 8px; }
        .skill-pill { 
          padding: 6px 12px; 
          background: rgba(170, 59, 255, 0.08); 
          border: 1px solid rgba(170, 59, 255, 0.2); 
          border-radius: 8px; 
          font-size: 0.85rem;
          color: #c084fc;
        }

        .job-card {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 18px;
          background: var(--glass);
          border: 1px solid var(--border);
          border-radius: 16px;
          margin-bottom: 12px;
          transition: 0.2s;
        }
        .job-main h4 { margin: 0; font-size: 1.1rem; }
        .missing-list { display: flex; gap: 8px; margin-top: 6px; flex-wrap: wrap; }
        .m-item { font-size: 0.65rem; color: #f87171; background: rgba(248, 113, 113, 0.1); padding: 2px 6px; border-radius: 4px; display: flex; align-items: center; gap: 3px; }
        .perfect-match { font-size: 0.7rem; color: #10b981; font-weight: 700; }
        .score-box { text-align: right; display: flex; align-items: center; gap: 10px; }
        .score-num { font-size: 1.5rem; font-weight: 800; color: white; }

        .icon-pulse { animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

        @media (max-width: 900px) {
          .bento-grid, .results-grid { grid-template-columns: 1fr; }
          .hero-title { font-size: 2.5rem; }
        }
      `}</style>
    </div>
  );
};

export default App;