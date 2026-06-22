"""
graph-greener (simple version)
Generates backdated commits in the current git repo to fill your GitHub
contribution graph, then pushes them to the remote.

Usage:
    1. Run this INSIDE the local folder that is already a git repo
       (e.g. your cloned 'privet' folder), with a remote already set up.
    2. python main.py
"""

import os
import random
import subprocess
from datetime import datetime, timedelta

LOG_FILE = "contributions.txt"


def run(cmd):
    subprocess.run(cmd, shell=True, check=True)


def main():
    print("=" * 60)
    print("Welcome to graph-greener - GitHub Contribution Graph Commit Generator")
    print("=" * 60)
    print("This tool will help you fill your GitHub contribution graph with custom commits.\n")

    try:
        count = int(input("How many commits do you want to make (default 20): ") or 20)
    except ValueError:
        count = 20

    try:
        days_back = int(input("How many days back should commits span (default 365): ") or 365)
    except ValueError:
        days_back = 365

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("Contribution log\n")

    today = datetime.now()

    for i in range(count):
        random_days_ago = random.randint(0, days_back)
        commit_date = today - timedelta(days=random_days_ago)
        date_str = commit_date.strftime("%Y-%m-%dT%H:%M:%S")

        with open(LOG_FILE, "a") as f:
            f.write(f"Commit {i + 1} - {date_str}\n")

        run("git add .")
        env_date = f'set GIT_AUTHOR_DATE={date_str}&& set GIT_COMMITTER_DATE={date_str}&&'
        run(f'{env_date} git commit -m "Contribution commit {i + 1}"')

        print(f"[{i + 1}/{count}] Committed with date {date_str}")

    print("\nAll commits created locally.")
    push = input("Push to GitHub now? (y/n): ").strip().lower()
    if push == "y":
        run("git push")
        print("Pushed successfully.")
    else:
        print("Skipped push. Run 'git push' manually when ready.")


if __name__ == "__main__":
    main()