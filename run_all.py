import subprocess, sys, os
root = os.path.dirname(os.path.abspath(__file__))
steps = ["python/00_check_environment.py", "python/01_load_to_duckdb.py", "python/02_run_checks.py"]
for s in steps:
    print(f"\n=== {s} ===")
    if subprocess.run([sys.executable, os.path.join(root, s)], cwd=os.path.join(root, "python")).returncode != 0:
        sys.exit(f"Stopped: {s} failed")
print("\nAll steps passed. Add analysis steps only AFTER docs/preregistration.md is committed.")
