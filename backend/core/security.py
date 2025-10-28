# backend/core/security.py
import subprocess
import os
from .logger import log_security, log_error

def bandit_scan(path: str) -> bool:
    """
    Run Bandit security scan on .py and .pyx files.
    """
    if not os.path.exists(path):
        log_error(f"[Bandit] Path does not exist: {path}")
        return False

    log_security(f"[Bandit] Scanning Python and Cython files in {path}...")

    # Build a list of Python/Cython files
    py_files = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith((".py", ".pyx")):
                py_files.append(os.path.join(root, f))

    if not py_files:
        log_security("[Bandit] No Python or Cython files found to scan")
        return True

    try:
        result = subprocess.run(
            ["bandit", "-r"] + py_files,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            log_security(result.stdout)
            log_security(result.stderr)
            log_security("[Bandit] Issues detected.")
            return False
        log_security("[Bandit] No issues detected.")
        return True
    except FileNotFoundError:
        log_error("[Bandit] bandit executable not found. Did you pip install bandit?")
        return False

def pip_audit_scan(requirements_path: str) -> bool:
    """
    Run pip-audit on a requirements.txt file.
    Returns True if no vulnerabilities, False otherwise.
    """
    if not os.path.exists(requirements_path):
        log_security(f"[pip-audit] No requirements.txt found at {requirements_path}")
        return True  # nothing to scan

    log_security(f"[pip-audit] Scanning {requirements_path}...")
    try:
        result = subprocess.run(
            ["pip-audit", "-r", requirements_path],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            log_security(result.stdout)
            log_security(result.stderr)
            log_security("[pip-audit] Vulnerabilities detected.")
            return False
        log_security("[pip-audit] No vulnerabilities found.")
        return True
    except FileNotFoundError:
        log_error("[pip-audit] pip-audit executable not found. Did you pip install pip-audit?")
        return False
