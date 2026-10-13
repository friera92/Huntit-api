"""Build a clean source ZIP and compare it with the two supplied original archives."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import zipfile


EXCLUDED_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".angular", "dist",
                 "tmp", "coverage", "out-tsc", "staticfiles", ".pytest_cache", ".idea"}


def excluded(path):
    parts = tuple(part.casefold() for part in PurePosixPath(path).parts)
    name = parts[-1]
    return (any(part in EXCLUDED_DIRS for part in parts)
            or name.startswith(".local-secret-key")
            or (name.startswith(".env") and name != ".env.example")
            or ".sqlite" in name or name.endswith(".db") or ".db." in name or ".db-" in name
            or any(extension + "." in name for extension in (".pem", ".key", ".pfx", ".p12"))
            or name.endswith((".pyc", ".pyo", ".sqlite3", ".sqlite3-journal", ".sqlite3-wal",
                              ".sqlite3-shm", ".log", ".pem", ".key", ".pfx", ".p12", ".crt", ".cer")))


def files(root):
    for directory, dirs, names in os.walk(root):
        for name in dirs:
            path = Path(directory) / name
            if name.casefold() not in EXCLUDED_DIRS and (path.is_symlink() or path.is_junction()):
                raise SystemExit(f"Linked directories are not packaged: {path}")
        dirs[:] = sorted(name for name in dirs if name.casefold() not in EXCLUDED_DIRS)
        for name in sorted(names):
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            if not excluded(relative):
                if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                    raise SystemExit(f"Linked files are not packaged: {relative}")
                with path.open("rb") as content:
                    if content.read(16) == b"SQLite format 3\x00":
                        continue
                yield relative, path


def comparison(archive, prefix, root):
    original, ignored = {}, []
    with zipfile.ZipFile(archive) as source:
        for item in source.infolist():
            if item.is_dir():
                continue
            relative = PurePosixPath(item.filename).parts[1:]
            target = str(PurePosixPath(prefix, *relative))
            if excluded(target):
                ignored.append(target)
            else:
                original[target] = source.read(item)
    unchanged, modified, missing = [], [], []
    for name, data in sorted(original.items()):
        path = root / name
        if not path.is_file():
            missing.append(name)
        elif path.read_bytes() == data:
            unchanged.append(name)
        else:
            modified.append(name)
    return {
        "archive": archive.name,
        "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
        "unchanged_count": len(unchanged), "modified_count": len(modified),
        "unchanged_files": unchanged, "modified_files": modified,
        "missing_files": missing, "excluded_local_state": sorted(ignored),
    }, set(original)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frontend-original", type=Path, required=True)
    parser.add_argument("--backend-original", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--manifest-output", type=Path,
                        help="Optional comparison report outside the project; not bundled in the ZIP.")
    options = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    frontend, front_names = comparison(options.frontend_original, "", root)
    backend, back_names = comparison(options.backend_original, "backend", root)
    if frontend["missing_files"] or backend["missing_files"]:
        raise SystemExit("An original source file is missing; inspect the comparison before packaging.")
    release_files = dict(files(root))
    added = sorted(set(release_files) - front_names - back_names)
    manifest = {
        "comparison": "Byte-for-byte source comparison; backend relocated under backend/.",
        "ddinza_frontend": frontend, "leduan_backend": backend,
        "added_files": added, "added_count": len(added),
        "excluded_from_release": sorted(EXCLUDED_DIRS) + [
            "SQLite databases and journals", "local secrets and .env", "TLS keys/certificates", "logs"],
    }
    if options.manifest_only and not options.manifest_output:
        parser.error("--manifest-only requires --manifest-output outside the project.")
    if options.manifest_output:
        if Path(os.path.abspath(options.manifest_output)).resolve().is_relative_to(root):
            parser.error("Choose a comparison report output outside the project.")
        options.manifest_output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Original frontend: {len(front_names)} files; {len(frontend['modified_files'])} modified.")
    print(f"Original backend source: {len(back_names)} files; {len(backend['modified_files'])} modified.")
    print(f"Added files: {len(added)}. Original source files removed: 0.")
    if options.manifest_only:
        return
    output = options.output or root.parent / "HuntIt-integrated.zip"
    if output.resolve().is_relative_to(root):
        raise SystemExit("Choose a ZIP output outside the project folder.")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, path in files(root):
            archive.write(path, f"HuntIt-integrated/{relative}")
    checksum = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(".zip.sha256").write_text(f"{checksum}  {output.name}\n", encoding="ascii")
    print(f"Created {output} ({output.stat().st_size:,} bytes), SHA-256 {checksum}")


if __name__ == "__main__":
    main()
