import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .logger import log_info, log_error, log_module
from .module_loader import load_all_modules
from sdk.decorators import NODE_REGISTRY

class ModuleChangeHandler(FileSystemEventHandler):
    """
    Watch for .py and .pyx changes in modules folder,
    clear NODE_REGISTRY, reload modules, and log output.
    """
    def __init__(self, modules_dir: str):
        self.modules_dir = modules_dir

    def on_any_event(self, event):
        # Only react to Python or Cython files
        if not event.src_path.endswith((".py", ".pyx")):
            return
        log_info(f"Detected change in {event.src_path}")
        self.reload_modules()

    def reload_modules(self):
        try:
            # Clear existing nodes
            NODE_REGISTRY.clear()
            log_module("Cleared NODE_REGISTRY")
            # Reload modules (runs Bandit + pip-audit)
            modules = load_all_modules(self.modules_dir)
            log_info(f"Reloaded {len(modules)} modules.")
        except Exception as e:
            log_error(f"Error reloading modules: {e}")

def start_reloader(modules_dir: str):
    """
    Start a daemon thread to watch the modules directory.
    """
    event_handler = ModuleChangeHandler(modules_dir)
    observer = Observer()
    observer.schedule(event_handler, modules_dir, recursive=True)

    def _run():
        observer.start()
        log_info(f"Watching for module changes in: {modules_dir}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
