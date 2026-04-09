function triggerFile() {
    document.getElementById("resume").click();
}

function upload() {
    const fileInput = document.getElementById("resume");
    const loader = document.getElementById("loader");

    if (fileInput.files.length === 0) {
        alert("Please select a file!");
        return;
    }

    loader.classList.remove("hidden");

    const formData = new FormData();
    formData.append("resume", fileInput.files[0]);

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        loader.classList.add("hidden");
        showScore(data.score);
        showSkills(data.skills);
        showJobs(data.jobs);
    });
}

function showScore(score) {
    document.getElementById("score").innerHTML =
        `<h2>🔥 Overall Score: ${score}%</h2>`;
}

function showSkills(skills) {
    document.getElementById("skills").innerHTML =
        `<h3>Skills:</h3> ${skills.join(", ")}`;
}

function showJobs(jobs) {
    const container = document.getElementById("jobs");
    container.innerHTML = "";

    jobs.forEach(job => {
        container.innerHTML += `
            <div class="card">
                <h3>${job.role}</h3>
                <p>${job.match}% Match</p>

                <div class="progress">
                    <div class="progress-bar" style="width:${job.match}%"></div>
                </div>

                <p>Missing: ${job.missing.join(", ") || "None"}</p>
            </div>
        `;
    });
}