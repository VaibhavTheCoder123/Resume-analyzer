function JobCard({ job }) {
  return (
    <div className="card">
      <h3>{job.role}</h3>

      <div className="progress">
        <div
          className="progress-bar"
          style={{ width: `${job.match}%` }}
        ></div>
      </div>

      <p>{job.match}% Match</p>

      <p className="missing">
        Missing: {job.missing.length ? job.missing.join(", ") : "None"}
      </p>
    </div>
  );
}

export default JobCard;