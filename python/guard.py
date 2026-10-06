"""Refuses to run analysis until the pre-registration is committed (no peeking)."""
import subprocess, sys
def require_committed(root, rel_paths):
    def git(*a):
        return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True)
    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        sys.exit("Not a git repo. Run 'git init' and commit your pre-registration first.")
    for p in rel_paths:
        if not git("log", "--oneline", "--", p).stdout.strip():
            sys.exit(f"{p} has never been committed. Commit it BEFORE running the analysis.")
        if git("status", "--porcelain", "--", p).stdout.strip():
            sys.exit(f"{p} has uncommitted changes. Commit it (log changes under 'Amendments').")
