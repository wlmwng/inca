import os as _os
from importlib import import_module

_expected_file_end = "_scraper.py"

__all__ = [
    fname
    for fname in _os.listdir("usmedia_scrapers")
    if fname[-len(_expected_file_end) :] == _expected_file_end
    and not fname.startswith(".")
]

for module in __all__:
    __import__(".".join(["inca.usmedia_scrapers", module.replace(".py", "")]))
