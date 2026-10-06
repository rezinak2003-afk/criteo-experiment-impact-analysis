import importlib, sys
print("Python", sys.version.split()[0])
ok = True
for m in ["pandas", "numpy", "scipy", "statsmodels", "matplotlib", "duckdb", "pytest"]:
    try:
        mod = importlib.import_module(m)
        print(f"OK   {m} {getattr(mod, '__version__', '')}")
    except ImportError:
        ok = False
        print(f"FAIL {m} (run: pip install -r requirements.txt)")
sys.exit(0 if ok else 1)
