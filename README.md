# GraphFlow Cython Demo

## 🧩 What is this?
A tiny prototype showing how your FastAPI + Cython + module loader workflow could work together.

---

## 🚀 Setup (Explain Like I'm 5)
1️⃣ Install Python 3.11+  
2️⃣ Open a terminal and run:

```bash
pip install cython setuptools wheel fastapi uvicorn pytest
```

3️⃣ Build the Cython module:

```bash
python cython_build/setup_cython.py build_ext --inplace
```

4️⃣ Run the backend server:

```bash
python backend/main.py
```

Then open your browser to **http://127.0.0.1:8000/ui**

5️⃣ Run tests:

```bash
pytest -v
```

---

### 💡 Notes
- `image_filter.pyx` → compiled Cython version of the module  
- `main.py` → fallback pure Python version  
- `module_loader.py` → loads compiled `.so/.pyd` first, falls back to `.py`  
- `project_manager.py` → handles per-project virtual environments (placeholder)  
- Future: Add Bandit & pip-audit scanning during module upload

---

## 🔒 Why Cython?
- Makes your core logic harder to reverse engineer
- Optionally speeds up CPU-heavy work

Keep user-created modules in **plain Python** for security scanning and community contribution.

---

## 🧱 Folder Structure

```
graphflow_cython_demo/
├── backend/
│   └── core/
├── projects/demo_project/modules/image_filter/
├── cython_build/
└── tests/
```

---

Have fun hacking 🚀
