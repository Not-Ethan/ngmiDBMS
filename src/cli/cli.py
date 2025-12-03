from src.cli.ui.cli_ui import UI, console
from src.cli.ui.spinner import loading
from src.services.auth_service import register_user, login_user, get_current_user, logout_user
from src.services.resume_service.resume_service import ResumeService
from src.services.job_service import list_jobs, get_job_details, apply_to_job, get_user_applications, get_ngmi_history

resume_service = ResumeService()


def require_login(func):
    def wrapper(*args, **kwargs):
        if not get_current_user():
            UI.error("You must be logged in to use this command.")
            return
        return func(*args, **kwargs)
    return wrapper


# AUTH --------------------------------------------------------------------

def cmd_register():
    UI.section("Register New Account")
    email = UI.prompt("Email")
    full_name = UI.prompt("Full Name")
    password = UI.prompt("Password")

    try:
        user_id = register_user(email, full_name, password)
        UI.success(f"User registered successfully (ID: {user_id})")
    except ValueError as e:
        UI.error(str(e))


def cmd_login():
    UI.section("Login")
    email = UI.prompt("Email")
    password = UI.prompt("Password")

    try:
        user = login_user(email, password)
        UI.success(f"Welcome back, {user['full_name']}!")
    except ValueError as e:
        UI.error(str(e))


def cmd_logout():
    logout_user()
    UI.success("You have been logged out.")


# RESUMES -----------------------------------------------------------------

@require_login
def cmd_upload_resume():
    UI.section("Upload Resume")
    file_path = UI.prompt("PDF Resume Path")

    try:
        user = get_current_user()

        with loading("Extracting and parsing resume...", spinner="dots"):
            resume_id = resume_service.upload_resume(user["user_id"], file_path)

        resume = ResumeService.get_resume_details(resume_id)
        skills = ", ".join(resume.get("skills", []))

        UI.panel(
            "Resume Upload Complete",
            f"[bold white]Resume ID:[/] {resume_id}\n"
            f"[bold white]Detected Skills:[/] {skills}"
        )

    except Exception as e:
        UI.error(str(e))


@require_login
def cmd_list_resumes():
    user = get_current_user()
    resumes = ResumeService.get_user_resumes(user["user_id"])

    if not resumes:
        UI.error("You have no resumes uploaded.")
        return

    from rich.table import Table
    table = Table(title="Your Resumes", border_style="magenta")
    table.add_column("ID", style="bold white")
    table.add_column("File Name")
    table.add_column("Uploaded At")

    for r in resumes:
        table.add_row(str(r["resume_id"]), r["file_name"], str(r["uploaded_at"]))

    console.print(table)


@require_login
def cmd_view_resume():
    resume_id = UI.prompt("Resume ID")

    try:
        resume = ResumeService.get_resume_details(int(resume_id))
        if not resume:
            UI.error("Resume not found.")
            return

        UI.panel(
            resume["file_name"],
            f"[white]Uploaded:[/] {resume['uploaded_at']}\n"
            f"[white]Skills:[/] {', '.join(resume.get('skills', []))}\n\n"
            f"[white]Preview:[/]\n{resume['raw_text'][:300]}..."
        )

    except Exception as e:
        UI.error(str(e))


# JOBS ---------------------------------------------------------------------

def cmd_list_jobs():
    jobs = list_jobs()

    from rich.table import Table
    table = Table(title="Available Jobs", border_style="magenta")
    table.add_column("ID", style="white bold")
    table.add_column("Title")
    table.add_column("Company")

    for j in jobs:
        table.add_row(str(j["job_id"]), j["title"], j["company"])

    console.print(table)


def cmd_view_job():
    job_id = UI.prompt("Job ID")

    try:
        job = get_job_details(int(job_id))
        if not job:
            UI.error("Job not found.")
            return

        UI.panel(
            f"{job['title']} at {job['company']}",
            job["description"]
        )

    except Exception as e:
        UI.error(str(e))


# APPLICATIONS ------------------------------------------------------------

@require_login
def cmd_apply():
    UI.section("Apply to Job")

    job_id = UI.prompt("Job ID")
    resume_id = UI.prompt("Resume ID")

    try:
        user = get_current_user()

        with loading("Processing NGMI evaluation...", spinner="dots"):
            app_id = apply_to_job(user["user_id"], int(job_id), int(resume_id))

        ngmi = get_ngmi_history(app_id)

        UI.panel(
            "Application Submitted",
            f"[bold]NGMI Score:[/] {ngmi['ngmi_score']}\n"
            f"[bold]Comment:[/] {ngmi['ngmi_comment']}"
        )

    except Exception as e:
        UI.error(str(e))


@require_login
def cmd_my_applications():
    user = get_current_user()
    apps = get_user_applications(user["user_id"])

    if not apps:
        UI.error("No applications found.")
        return

    from rich.table import Table
    table = Table(title="Your Applications", border_style="magenta")
    table.add_column("ID", style="white bold")
    table.add_column("Job")
    table.add_column("Company")
    table.add_column("NGMI Score")

    for a in apps:
        table.add_row(
            str(a["application_id"]),
            a["title"],
            a["company"],
            str(a["ngmi_score"])
        )

    console.print(table)


def cmd_help():
    UI.section("Available Commands")

    from rich.table import Table
    table = Table(show_header=False, border_style="magenta")
    table.add_column("Command", style="bold magenta")
    table.add_column("Description", style="white")

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
        'exit': 'Exit ngmiDBMS'
    }

    for cmd, desc in commands.items():
        table.add_row(cmd, desc)

    console.print(table)
    
@require_login
def cmd_ngmi_history():
    UI.section("NGMI Evaluation Details")

    app_id = UI.prompt("Application ID")

    try:
        ngmi = get_ngmi_history(int(app_id))

        if not ngmi:
            UI.error("No NGMI record found for that application.")
            return

        UI.panel(
            f"Application #{app_id}",
            f"[bold white]Job:[/] {ngmi['title']} at {ngmi['company']}\n"
            f"[bold white]Resume:[/] {ngmi['file_name']}\n"
            f"[bold white]NGMI Score:[/] {ngmi['ngmi_score']}\n"
            f"[bold white]Comment:[/]\n{ngmi['ngmi_comment']}\n"
            f"[bold white]Generated:[/] {ngmi['generated_at']}"
        )

    except Exception as e:
        UI.error(str(e))


def run_cli():
    UI.banner()
    console.print("[bold cyan]Type 'help' to see commands.[/]\n")

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
        'help': cmd_help,
    }

    while True:
        try:
            user = get_current_user()
            prefix = f"({user['email']}) " if user else ""
            cmd = UI.prompt(f"{prefix}>").lower().strip()

            if cmd == "exit":
                UI.info("Goodbye!")
                break

            if cmd in commands:
                commands[cmd]()
            else:
                UI.error(f"Unknown command '{cmd}'")

        except KeyboardInterrupt:
            console.print()
            UI.info("Exiting...")
            break

        except Exception as e:
            UI.error(str(e))
