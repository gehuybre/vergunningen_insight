import subprocess
import datetime
import os

def git_push():
    """Automates adding, committing, and pushing to GitHub with a timestamped message."""

    try:
        # Get the current date and time
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Automated commit - {timestamp}"

         # Add all changes
        subprocess.run(["git", "add", "."], check=True)

        # Commit with a timestamped message
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push to the main branch
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("Git push successful!")
        
    except subprocess.CalledProcessError as e:
        print(f"Git push failed. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    git_push()