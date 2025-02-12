import sys
from collections import deque
from typing import Any


import sys
import inspect
from collections import deque
from typing import Any


def memory_report(obj: Any) -> None:
    """
    Prints a memory report for the given object, including
    the total memory used and the module where the object is defined.

    Args:
        obj (Any): The object to generate a memory report for.

    Returns:
        None
    """
    # Получаем модуль, в котором объявлен объект
    module = inspect.getmodule(obj)
    module_name = module.__name__ if module else "Unknown module"

    # Create a set to keep track of objects that have already been processed
    seen = set()
    total_size = 0
    queue = deque([(obj, "root")])

    print(f"\n📊 Memory Report for: {obj.__class__.__name__}")
    print(f"📍 Module: {module_name}")
    print("-" * 50)

    while queue:
        current_obj, path = queue.popleft()

        if id(current_obj) in seen:
            continue

        seen.add(id(current_obj))
        size = sys.getsizeof(current_obj)
        total_size += size
        print(f"{path}: {size} bytes ({type(current_obj)})")

        if hasattr(current_obj, "__dict__"):
            for attr, value in vars(current_obj).items():
                queue.append((value, f"{path}.{attr}"))
        elif isinstance(current_obj, (list, tuple, set)):
            for i, item in enumerate(current_obj):
                queue.append((item, f"{path}[{i}]"))
        elif isinstance(current_obj, dict):
            for key, value in current_obj.items():
                queue.append((key, f"{path}.key({key})"))
                queue.append((value, f"{path}[{key}]"))

    print("-" * 50)
    print(f"🟢 Total Memory Used: {total_size}")
    print("*" * 50)
