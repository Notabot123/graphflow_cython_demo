import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import os, sys

sys.path.append(os.path.abspath("."))

from backend.core.project_manager import activate_project_env
from backend.core.module_loader import load_all_modules
from backend.core.reloader import start_reloader
import sdk.decorators  # NODE_REGISTRY

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Determine modules path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_path = os.path.join(BASE_DIR, "projects", "demo_project")
    modules_dir = os.path.join(project_path, "modules")

    # Activate venv & load modules
    activate_project_env(project_path)
    load_all_modules(modules_dir)

    # Start hot-reload watcher
    start_reloader(modules_dir)

    yield  # app runs

app = FastAPI(title="GraphFlow Cython Demo", lifespan=lifespan)

# API endpoint
@app.get("/api/nodes")
def list_nodes():
    from sdk.decorators import NODE_REGISTRY
    return {"nodes": list(NODE_REGISTRY.values())}

# UI endpoint
@app.get("/ui", response_class=HTMLResponse)
def ui_page():
    from sdk.decorators import NODE_REGISTRY
    html_nodes = "".join(
        f"<li>{n['name']} — <em>{n['category']}</em></li>"
        for n in NODE_REGISTRY.values()
    )
    return f"""
    <html>
        <head><title>GraphFlow Nodes</title></head>
        <body style='font-family:sans-serif; padding:2em'>
            <h1>Registered Nodes</h1>
            <ul>{html_nodes}</ul>
            <p><a href='/api/nodes'>View JSON</a></p>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
