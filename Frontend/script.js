function upload() {
    const fileInput = document.getElementById("resume");

    if (fileInput.files.length === 0) {
        alert("Select a file first!");
        return;
    }

    const formData = new FormData();
    formData.append("resume", fileInput.files[0]);

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        showSkills(data.skills);
        showJobs(data.jobs);
    });
}

function showSkills(skills) {
    const div = document.getElementById("skills");
    div.innerHTML = "<h2>Skills</h2>" + skills.join(", ");
}

function showJobs(jobs) {
    const container = document.getElementById("jobs");
    container.innerHTML = "<h2>Job Matches</h2>";

    jobs.forEach(job => {
        container.innerHTML += `
            <div class="card">
                <h3>${job.role}</h3>
                <p>Match: ${job.match}%</p>

                <div class="progress">
                    <div class="progress-bar" style="width:${job.match}%"></div>
                </div>

                <p>Missing: ${job.missing.join(", ") || "None"}</p>
            </div>
        `;
    });
}