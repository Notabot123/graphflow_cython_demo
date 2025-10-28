import importlib.util, os, sys, glob
from sdk.decorators import NODE_REGISTRY
from core.security import bandit_scan, pip_audit_scan

def import_compiled_extension_if_exists(module_path, pkg_name):
    for ext in ("*.so", "*.pyd"):
        files = glob.glob(os.path.join(module_path, ext))
        if files:
            compiled_file = files[0]
            spec = importlib.util.spec_from_file_location(f"{pkg_name}.image_filter", compiled_file)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mod
            spec.loader.exec_module(mod)
            print(f"[MODULE] Loaded compiled extension: {compiled_file}")
            return True
    return False

def load_all_modules(modules_dir: str):
    NODE_REGISTRY.clear()

    for name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, name)
        main_file = os.path.join(module_path, "main.py")
        if not os.path.isdir(module_path):
            continue

        bandit_scan(module_path)
        pip_audit_scan(os.path.join(module_path, "requirements.txt"))

        pkg_name = f"projects.demo_project.modules.{name}"
        compiled_loaded = import_compiled_extension_if_exists(module_path, pkg_name)
        if compiled_loaded:
            continue

        if os.path.isfile(main_file):
            spec = importlib.util.spec_from_file_location(f"{name}.main", main_file)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mod
            spec.loader.exec_module(mod)
            print(f"[MODULE] Loaded (py): {name}")
        else:
            print(f"[MODULE] No main.py found for {name}, skipping.")

    print(f"[INFO] Registered {len(NODE_REGISTRY)} nodes.")
    return NODE_REGISTRY
