# GraphFlow Cython Demo

## What is this?
A tiny prototype showing how your FastAPI + Cython + module loader workflow could work together.

---

## Setup
1️⃣ Install Python 3.11+  
2️⃣ Open a terminal and run:

```bash
pip install cython setuptools wheel fastapi uvicorn pytest colorama httpx bandit pip-audit

```
for hot reload, using reloader.py

```bash
pip install watchdog

```

3️⃣ Build the Cython module:

```bash
python cython_build/setup_cython.py build_ext --inplace
```

4️⃣ Run the backend server:

```bash
python backend/main.py
```
or alternatively:
```bash
python -m  backend.main
```

Then open your browser to:

**http://127.0.0.1:8000/ui**
 → friendly HTML list

**http://127.0.0.1:8000/api/nodes**
 → JSON of all loaded nodes

5️⃣ Run tests:

```bash
pytest -v
```

---
## Hot-reloading

Any changes to .py or .pyx files inside your modules folder are detected automatically.

NODE_REGISTRY is cleared and modules reloaded.

Logs in console show what was loaded.

## Adding a custom module

Create a folder inside projects/demo_project/modules/, e.g.:

projects/demo_project/modules/my_node/


Add your .py or .pyx file inside, e.g., main.py:
```python
from sdk.decorators import graph_node

@graph_node(
    name="Hello Node",
    category="Example",
    icon="👋",
    ui={"inputs": ["name"], "outputs": ["greeting"], "html": "<input name='name'>"}
)
def hello(name):
    return f"Hello, {name}!"
```

Optional: add requirements.txt if your module needs external libraries:

```bash
numpy>=1.25.0
```

Save the file — Watchdog will reload automatically. Check /ui and /api/nodes


### Notes
- `image_filter.pyx` → compiled Cython version of the module  
- `main.py` → fallback pure Python version  
- `module_loader.py` → loads compiled `.so/.pyd` first, falls back to `.py`  
- `project_manager.py` → handles per-project virtual environments (placeholder)  
- Bandit & pip-audit scanning during module upload
- Hot-reload is intended for development; in production you may disable it.

---

## Why Cython?
- Makes core logic harder to reverse engineer
- Optionally speeds up CPU-heavy work

Keep user-created modules in **plain Python** for security scanning and community contribution.

---

## Folder Structure

```
graphflow_cython_demo/
├── backend/
│   ├── core/
│   │   ├── module_loader.py
│   │   ├── project_manager.py
│   │   └── security.py      ← new
│   └── main.py
├── sdk/
│   ├── __init__.py
│   └── decorators.py
...

├── projects/demo_project/modules/image_filter/
├── cython_build/
└── tests/
```

---


