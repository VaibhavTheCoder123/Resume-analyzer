import { useState } from "react";

function UploadBox({ onUpload }) {
  const [file, setFile] = useState(null);

  return (
    <div className="upload-box">
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={() => onUpload(file)}>
        Analyze Resume
      </button>
    </div>
  );
}

export default UploadBox;