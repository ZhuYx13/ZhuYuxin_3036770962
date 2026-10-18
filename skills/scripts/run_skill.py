import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[2]
    subprocess.run([sys.executable, str(root / "code" / "run_all.py")], check=True)


if __name__ == "__main__":
    main()
