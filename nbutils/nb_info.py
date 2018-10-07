"""Import notebooks and allow us to manipulate them.
"""
from importlib import import_module


def import_notebook(package_name):
    nb = import_module(package_name)
    return nb.info, nb.image
