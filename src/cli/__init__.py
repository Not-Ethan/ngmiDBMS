import getpass
from src.services.auth_service import register_user, login_user, get_current_user, logout_user
from src.services.resume_service.resume_service import ResumeService
from src.services.job_service import list_jobs, get_job_details, apply_to_job, get_user_applications, get_ngmi_history

resume_service = ResumeService()

def require_login(func):
    def wrapper(*args, **kwargs):
        if not get_current_user():
            print("Please login first.")
            return
        return func(*args, **kwargs)
    return wrapper

def cmd_register():
    email = input("Email: ")
    full_name = input("Full name: ")
    password = getpass.getpass("Password: ")
    
    try:
        user_id = register_user(email, full_name, password)
        print(f"User registered successfully (ID: {user_id})")
    except ValueError as e:
        print(f"Registration failed: {e}")

def cmd_login():
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    
    try:
        user = login_user(email, password)
        print(f"Welcome back, {user['full_name']}!")
    except ValueError as e:
        print(f"Login failed: {e}")

def cmd_logout():
    logout_user()
    print("Logged out successfully.")

@require_login
def cmd_upload_resume():
    file_path = input("Resume file path: ")
    
    try:
        user = get_current_user()
        print("Extracting text...")
        resume_id = resume_service.upload_resume(user['user_id'], file_path)
        
        resume = ResumeService.get_resume_details(resume_id)
        skills = resume.get('skills', [])
        print(f"Detected skills: {', '.join(skills)}")
        print(f"Resume uploaded (ID = {resume_id})")
    except Exception as e:
        print(f"Upload failed: {e}")

@require_login
def cmd_list_resumes():
    user = get_current_user()
    resumes = ResumeService.get_user_resumes(user['user_id'])
    
    if not resumes:
        print("No resumes found.")
        return
    
    print("\nYour Resumes:")
    for resume in resumes:
        print(f"ID: {resume['resume_id']} | {resume['file_name']} | Uploaded: {resume['uploaded_at']}")

@require_login
def cmd_view_resume():
    try:
        resume_id = int(input("Resume ID: "))
        resume = ResumeService.get_resume_details(resume_id)
        
        if not resume:
            print("Resume not found.")
            return
        
        print(f"\nResume: {resume['file_name']}")
        print(f"Uploaded: {resume['uploaded_at']}")
        print(f"Skills: {', '.join(resume.get('skills', []))}")
        print(f"\nText preview: {resume['raw_text'][:200]}...")
    except ValueError:
        print("Invalid resume ID.")

def cmd_list_jobs():
    jobs = list_jobs()
    
    print("\nAvailable Jobs:")
    for job in jobs:
        print(f"ID: {job['job_id']} | {job['title']} at {job['company']}")

def cmd_view_job():
    try:
        job_id = int(input("Job ID: "))
        job = get_job_details(job_id)
        
        if not job:
            print("Job not found.")
            return
        
        print(f"\nJob: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Description: {job['description']}")
    except ValueError:
        print("Invalid job ID.")

@require_login
def cmd_apply():
    try:
        job_id = int(input("Job ID: "))
        resume_id = int(input("Resume ID: "))
        
        user = get_current_user()
        print("Generating NGMI evaluation...")
        
        application_id = apply_to_job(user['user_id'], job_id, resume_id)
        
        ngmi = get_ngmi_history(application_id)
        print(f"NGMI Score: {ngmi['ngmi_score']:.1f}")
        print(f"NGMI Comment: \"{ngmi['ngmi_comment']}\"")
        print("Application submitted.")
        
    except ValueError as e:
        print(f"Application failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

@require_login
def cmd_my_applications():
    user = get_current_user()
    applications = get_user_applications(user['user_id'])
    
    if not applications:
        print("No applications found.")
        return
    
    print("\nYour Applications:")
    for app in applications:
        print(f"ID: {app['application_id']} | {app['title']} at {app['company']}")
        print(f"  Applied: {app['applied_at']} | Status: {app['status']}")
        print(f"  NGMI: {app['ngmi_score']:.1f}")
        print(f"  \"{app['ngmi_comment']}\"\n")

def cmd_ngmi_history():
    try:
        app_id = int(input("Application ID: "))
        ngmi = get_ngmi_history(app_id)
        
        if not ngmi:
            print("Application not found.")
            return
        
        print(f"\nApplication to {ngmi['title']} at {ngmi['company']}")
        print(f"Resume: {ngmi['file_name']}")
        print(f"NGMI Score: {ngmi['ngmi_score']:.1f}")
        print(f"NGMI Comment: \"{ngmi['ngmi_comment']}\"")
        print(f"Generated: {ngmi['generated_at']}")
        
    except ValueError:
        print("Invalid application ID.")

def cmd_help():
    commands = {
        'register': 'Register new user',
        'login': 'Login to your account',
        'logout': 'Logout from your account',
        'upload_resume': 'Upload a resume file',
        'list_resumes': 'List your uploaded resumes',
        'view_resume': 'View resume details',
        'list_jobs': 'List available job postings',
        'view_job': 'View job posting details',
        'apply': 'Apply to a job with your resume',
        'my_applications': 'View your job applications',
        'ngmi_history': 'View NGMI details for an application',
        'help': 'Show this help message',
        'exit': 'Exit the application'
    }
    
    print("\nAvailable commands:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<15} - {desc}")

def run_cli():
    print("Welcome to ngmiDBMS - Your satirical job application tracker!")
    print("Type 'help' for available commands.")
    
    commands = {
        'register': cmd_register,
        'login': cmd_login,
        'logout': cmd_logout,
        'upload_resume': cmd_upload_resume,
        'list_resumes': cmd_list_resumes,
        'view_resume': cmd_view_resume,
        'list_jobs': cmd_list_jobs,
        'view_job': cmd_view_job,
        'apply': cmd_apply,
        'my_applications': cmd_my_applications,
        'ngmi_history': cmd_ngmi_history,
        'help': cmd_help
    }
    
    while True:
        try:
            user = get_current_user()
            prompt = f"({user['email']}) > " if user else "> "
            command = input(prompt).strip().lower()
            
            if command == 'exit':
                print("Goodbye!")
                break
            elif command in commands:
                commands[command]()
            elif command:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")