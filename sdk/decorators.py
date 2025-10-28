# sdk/decorators.py
from functools import wraps

NODE_REGISTRY = {}

def graph_node(name, category, icon=None, ui=None):
    """
    Decorator that registers a function as a graph node.
    """
    def decorator(func):
        NODE_REGISTRY[func.__name__] = {
            "name": name,
            "category": category,
            "icon": icon,
            "ui": ui or {},
            "function": func,
        }
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
