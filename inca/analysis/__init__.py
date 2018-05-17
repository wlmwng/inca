import os as _os

_expected_file_end = "_analysis.py"

__all__ = [fname for fname in _os.listdir('analysis') if fname[-len(_expected_file_end):]==_expected_file_end]

for module in __all__:
    __import__('.'.join(['analysis',module.replace('.py','')]))
