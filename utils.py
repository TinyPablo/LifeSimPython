from functools import wraps
import time
from datetime import datetime
from os import name as os_name
import importlib.util
import pathlib


def timeit(method):
    @wraps(method)
    def timed(*args, **kwargs):
        start_time = time.perf_counter()
        result = method(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f'({elapsed_time:.10f})')
        return result
    return timed


def get_time_now() -> str:
    now = datetime.now()
    if os_name == 'posix':
        return now.strftime("%d-%m-%Y %H:%M:%S")
    elif os_name == 'nt':
        return now.strftime("%d-%m-%Y %H_%M_%S")
    else:
        raise OSError()
    

def load_selection_condition_module(name: str):
    if not name:
        raise ValueError("No selection condition name provided")

    base = pathlib.Path(__file__).resolve().parent
    module_path = base / "selection_conditions" / f"{name}.py"

    if not module_path.exists():
        raise FileNotFoundError(f"Selection condition file not found: {module_path}")

    spec = importlib.util.spec_from_file_location(f"selection_conditions.{name}", str(module_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create import spec for {name}")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod