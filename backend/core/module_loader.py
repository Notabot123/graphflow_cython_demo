# backend/core/module_loader.py
import importlib.util
import os
import sys
from .logger import log_info, log_error, log_module
from .security import bandit_scan, pip_audit_scan

def load_all_modules(modules_dir: str):
    """
    Dynamically import all Python or Cython modules from the given directory.
    Returns a list of module objects.
    """
    loaded_modules = []

    if not os.path.isdir(modules_dir):
        log_error(f"Modules directory not found: {modules_dir}")
        return []

    log_info(f"Scanning modules in {modules_dir}")

    # Run placeholder security checks
    bandit_scan(modules_dir)
    pip_audit_scan(os.path.join(modules_dir, "requirements.txt"))


    for root, _, files in os.walk(modules_dir):
        for filename in files:
            if not (filename.endswith(".py") or filename.endswith(".pyd") or filename.endswith(".so")):
                continue

            mod_path = os.path.join(root, filename)

            # 👇 Derive module name from folder if it's a "main.py"
            folder_name = os.path.basename(root)
            base_name = os.path.splitext(filename)[0]

            if base_name == "main":
                mod_name = folder_name
            else:
                mod_name = base_name

            try:
                spec = importlib.util.spec_from_file_location(mod_name, mod_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[mod_name] = module
                    spec.loader.exec_module(module)
                    loaded_modules.append(module)
                    log_module(f"Loaded module: {mod_name}")
            except Exception as e:
                log_error(f"Failed to load {mod_name}: {e}")


    log_info(f"Total modules loaded: {len(loaded_modules)}")
    return loaded_modules
