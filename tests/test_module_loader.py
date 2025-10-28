# tests/test_module_loader.py
import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.core import module_loader


def test_module_loader_runs():
    project_modules_path = os.path.abspath("projects/demo_project/modules")
    modules = module_loader.load_all_modules(project_modules_path)
    print("Loaded modules:", modules)  # for pytest output visibility
    assert isinstance(modules, list)

    # More informative assertion
    if not any("image_filter" in str(m) for m in modules):
        pytest.fail(f"No 'image_filter' found in loaded modules: {modules}")
