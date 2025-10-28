import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
import os, sys

sys.path.append(os.path.abspath("."))  # ensure sdk importable

from backend.core.project_manager import activate_project_env
from backend.core.module_loader import load_all_modules
import sdk.decorators  # 👈 ensure NODE_REGISTRY is created and ready


@asynccontextmanager
async def lifespan(app: FastAPI):
    project_path = os.path.abspath("projects/demo_project")
    activate_project_env(project_path)
    load_all_modules(os.path.join(project_path, "modules"))
    yield  # app runs


app = FastAPI(title="GraphFlow Cython Demo", lifespan=lifespan)


@app.get("/api/nodes")
def list_nodes():
    from sdk.decorators import NODE_REGISTRY
    return {"nodes": list(NODE_REGISTRY.values())}


@app.get("/ui")
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
