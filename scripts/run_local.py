"""Run Angular and Django locally and stop both when this command exits."""
import argparse
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import threading
import time


def child_environment(secure):
    environment = os.environ.copy()
    environment["HUNTIT_HTTPS"] = "true" if secure else "false"
    # Fresh Angular installs must not wait for an interactive CLI setup prompt.
    environment["NG_CLI_ANALYTICS"] = "false"
    environment["NG_FORCE_TTY"] = "false"
    environment["NG_FORCE_AUTOCOMPLETE"] = "false"
    return environment


def port_is_open(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.2):
            return True
    except OSError:
        return False


def ensure_ports_available(ports=(8000, 4200)):
    for port in ports:
        if port_is_open(port):
            raise RuntimeError(
                f"Port {port} is already in use. Stop the other HuntIt terminal "
                "with Ctrl+C, then run this command again."
            )


def forward_output(name, stream):
    try:
        for line in stream:
            message = f"[{name}] {line.rstrip()}"
            encoding = getattr(sys.stdout, "encoding", None)
            if encoding:
                # Windows redirected terminals may use cp1252 while Angular emits UTF-8.
                message = message.encode(encoding, errors="replace").decode(encoding)
            print(message, flush=True)
    finally:
        stream.close()


def wait_for_servers(servers, timeout=180):
    deadline = time.monotonic() + timeout
    while True:
        for name, process, port in servers:
            code = process.poll()
            if code is not None:
                raise RuntimeError(
                    f"{name} stopped during startup (exit code {code}). "
                    "Check its messages above."
                )
        if all(port_is_open(port) for _, _, port in servers):
            return
        if time.monotonic() >= deadline:
            raise RuntimeError(
                f"HuntIt did not finish starting within {timeout} seconds. "
                "Check the Django and Angular messages above, then try again."
            )
        time.sleep(0.25)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--http", action="store_true", help="Use loopback HTTP for development/browser QA.")
    parser.add_argument("--cert", help="Optional trusted localhost TLS certificate PEM file.")
    parser.add_argument("--key", help="TLS private key PEM file paired with --cert.")
    options = parser.parse_args()
    if bool(options.cert) != bool(options.key):
        parser.error("Provide both --cert and --key.")
    root = Path(__file__).resolve().parent.parent
    python = root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    angular = root / "node_modules" / "@angular" / "cli" / "bin" / "ng.js"
    node = shutil.which("node")
    database = Path(os.environ.get("HUNTIT_DATABASE", str(root / "backend" / "db.sqlite3")))
    if not python.exists() or not database.exists():
        raise SystemExit("Run python scripts/setup_local.py first.")
    if not node or not angular.exists():
        raise SystemExit("Install Node.js, then run npm ci in the project folder.")
    secure = not options.http
    environment = child_environment(secure)
    angular_command = [node, str(angular), "serve", "--host", "127.0.0.1", "--proxy-config",
                       "proxy.https.conf.json" if secure else "proxy.conf.json"]
    if secure:
        angular_command.extend(["--ssl", "true"])
        if options.cert:
            angular_command.extend(["--ssl-cert", options.cert, "--ssl-key", options.key])
    commands = [
        ("Django", [str(python), "-u", "backend/manage.py", "runserver", "127.0.0.1:8000", "--noreload"], 8000),
        ("Angular", angular_command, 4200),
    ]
    processes = []
    servers = []
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    try:
        ensure_ports_available()
        print("Starting Django and Angular. Wait for 'HuntIt is ready' before opening the app.", flush=True)
        print("The first frontend build may take a little longer. Startup messages appear below.", flush=True)
        for name, command, port in commands:
            process = subprocess.Popen(
                command, cwd=root, creationflags=flags,
                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace", bufsize=1, env=environment,
            )
            processes.append(process)
            servers.append((name, process, port))
            threading.Thread(target=forward_output, args=(name, process.stdout), daemon=True).start()
        wait_for_servers(servers)
        scheme = "https" if secure else "http"
        admin_url = f"{scheme}://127.0.0.1:4200/admin/" if secure else "http://127.0.0.1:8000/admin/"
        print(f"HuntIt is ready: {scheme}://127.0.0.1:4200/  |  Admin: {admin_url}", flush=True)
        if secure and not options.cert:
            print("Development TLS uses a self-signed certificate. Supply --cert and --key for a trusted certificate.", flush=True)
        print("Press Ctrl+C to stop both servers.", flush=True)
        while all(process.poll() is None for process in processes):
            time.sleep(0.5)
        name, stopped, _ = next(server for server in servers if server[1].returncode is not None)
        print(f"{name} stopped (exit code {stopped.returncode}). Stopping both servers.", flush=True)
        return stopped.returncode or 0
    except KeyboardInterrupt:
        return 0
    except (OSError, RuntimeError) as error:
        print(f"HuntIt could not start: {error}", file=sys.stderr, flush=True)
        return 1
    finally:
        for process in processes:
            if process.poll() is None:
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=10)


if __name__ == "__main__":
    sys.exit(main())
