import { useState } from "react";
import axios from "axios";
import UploadBox from "./components/UploadBox";
import JobCard from "./components/JobCard";
import "./App.css";

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadResume = async (file) => {
    const formData = new FormData();
    formData.append("resume", file);

    setLoading(true);

    const res = await axios.post("http://127.0.0.1:5000/upload", formData);
    setData(res.data);

    setLoading(false);
  };

  return (
    <div className="app">
      <div className="sidebar">
        <h2>AI Analyzer</h2>
        <p>Dashboard</p>
        <p>Insights</p>
      </div>

      <div className="main">
        <h1>Resume Intelligence</h1>

        <UploadBox onUpload={uploadResume} />

        {loading && <div className="loader"></div>}

        {data && (
          <>
            <div className="score">
              Score: {data.score}%
            </div>

            <div className="jobs">
              {data.jobs.map((job, i) => (
                <JobCard key={i} job={job} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;