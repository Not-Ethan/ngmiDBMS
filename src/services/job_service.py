from src.database import db
from src.services.ngmi_service import generate_ngmi

def list_jobs() -> list:
    return db.execute("SELECT * FROM JobPostings ORDER BY job_id")

def get_job_details(job_id: int):
    return db.execute_one("SELECT * FROM JobPostings WHERE job_id = %s", (job_id,))

def apply_to_job(user_id: int, job_id: int, resume_id: int) -> int:
    existing = db.execute_one(
        "SELECT application_id FROM Applications WHERE user_id = %s AND job_id = %s",
        (user_id, job_id)
    )
    if existing:
        raise ValueError("Already applied to this job")
    
    resume = db.execute_one("SELECT raw_text FROM Resumes WHERE resume_id = %s", (resume_id,))
    job = db.execute_one("SELECT description FROM JobPostings WHERE job_id = %s", (job_id,))
    
    if not resume or not job:
        raise ValueError("Resume or job not found")
    
    app_result = db.execute_one(
        "INSERT INTO Applications (user_id, job_id, resume_id) VALUES (%s, %s, %s) RETURNING application_id",
        (user_id, job_id, resume_id)
    )
    application_id = app_result['application_id']
    
    ngmi_score, ngmi_comment = generate_ngmi(resume['raw_text'], job['description'])
    
    db.execute(
        "INSERT INTO NGMIScores (application_id, ngmi_score, ngmi_comment) VALUES (%s, %s, %s)",
        (application_id, ngmi_score, ngmi_comment)
    )
    
    return application_id

def get_user_applications(user_id: int):
    return db.execute(
        """SELECT a.application_id, a.applied_at, a.status,
                  j.title, j.company,
                  n.ngmi_score, n.ngmi_comment
           FROM Applications a
           JOIN JobPostings j ON a.job_id = j.job_id
           LEFT JOIN NGMIScores n ON a.application_id = n.application_id
           WHERE a.user_id = %s
           ORDER BY a.applied_at DESC""",
        (user_id,)
    )

def get_ngmi_history(application_id: int):
    return db.execute_one(
        """SELECT a.application_id, j.title, j.company, j.description,
                  r.file_name, n.ngmi_score, n.ngmi_comment, n.generated_at
           FROM Applications a
           JOIN JobPostings j ON a.job_id = j.job_id
           JOIN Resumes r ON a.resume_id = r.resume_id
           JOIN NGMIScores n ON a.application_id = n.application_id
           WHERE a.application_id = %s""",
        (application_id,)
    )