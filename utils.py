from functools import wraps
import time
from datetime import datetime
from os import name as os_name

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
