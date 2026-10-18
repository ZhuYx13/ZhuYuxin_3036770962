import subprocess
import sys
from pathlib import Path


def run(script):
    print(f"Running {script.name} ...")
    subprocess.run([sys.executable, str(script)], check=True)


def main():
    root = Path(__file__).resolve().parents[1]
    for script in ["clean.py", "tables.py", "figure.py", "make_report.py"]:
        run(root / "code" / script)
    print("All outputs generated.")


if __name__ == "__main__":
    main()