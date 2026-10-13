"""Local secrets stay on each developer's computer instead of in the repository."""
from pathlib import Path
import secrets


def local_secret(base_dir: Path) -> str:
    path = base_dir / ".local-secret-key"
    try:
        with path.open("x", encoding="utf-8") as output:
            output.write(secrets.token_urlsafe(64))
    except FileExistsError:
        pass
    value = path.read_text(encoding="utf-8").strip()
    if not value:
        raise RuntimeError("The local Django secret file is empty; restore or regenerate it.")
    return value
