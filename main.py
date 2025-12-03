from src.database import db
from src.cli import run_cli

def main():
    try:
        print("Initializing ngmiDBMS...")
        db.setup_tables()
        print("Database initialized successfully.")
        run_cli()
    except Exception as e:
        print(f"Failed to start ngmiDBMS: {e}")
        print("Make sure PostgreSQL is running and configured correctly.")

if __name__ == "__main__":
    main()
