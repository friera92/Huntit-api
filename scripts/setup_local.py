"""Install the backend and create a local SQLite database without replacing data."""
import os
from pathlib import Path
import subprocess
import sys
import venv


def main():
    if sys.version_info < (3, 12):
        raise SystemExit("Use Python 3.12 or newer.")
    root = Path(__file__).resolve().parent.parent
    temporary = root / "tmp" / "setup"
    temporary.mkdir(parents=True, exist_ok=True)
    os.environ["TEMP"] = os.environ["TMP"] = os.environ["TMPDIR"] = str(temporary)
    environment = root / ".venv"
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        venv.EnvBuilder(with_pip=True).create(environment)
    subprocess.run([str(python), "-m", "ensurepip", "--upgrade"], check=True, cwd=root)
    subprocess.run([
        str(python), "-m", "pip", "install", "--disable-pip-version-check",
        "-r", str(root / "backend" / "requirements.txt"),
    ], check=True, cwd=root)
    for command in ["migrate", "seed_local_data", "check"]:
        subprocess.run([str(python), "backend/manage.py", command], check=True, cwd=root)
    print("Backend ready. Install the frontend with npm ci, then run python scripts/run_local.py.")
    print("Create your own administrator with .venv/Scripts/python.exe backend/manage.py createsuperuser (Windows).")


if __name__ == "__main__":
    main()
