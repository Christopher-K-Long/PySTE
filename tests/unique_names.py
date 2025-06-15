import os
import threading
import datetime
import inspect

def get_unique_name(level=0):
    thread_id = threading.current_thread().ident
    datetime.datetime.now().strftime("%Z%Y%m%d%H%M%S%f")
    return f"calling_function_{__name__}_{inspect.stack()[1+level][3]}__thread_id_{thread_id}__datetime_{datetime.datetime.now().strftime('%Z%Y%m%d%H%M%S%f')}"

class UniquePath():
    def __init__(self):
        self.unique_path = get_unique_name(1)+".pkl"
    def __enter__(self):
        return self.unique_path
    def __exit__(self, exception_type, exception_value, exception_traceback):
        if os.path.exists(self.unique_path):
            os.remove(self.unique_path)