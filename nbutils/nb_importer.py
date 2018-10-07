"""Import notebooks as regular python modules.

There is a lot of magic going here as we are going to override the way python imports
code. This is definitely my own creation, I have simply modified the code found on the
page linked below for my own use.

https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html
"""
import io
import os
import sys
import types

from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from nbformat import read


def find_notebook(fullname, path=None):
    """I think converts a module name a.b.c into a filepath a/b/c.ipynb"""

    print(fullname, path)
    name = fullname.rsplit('.', 1)[-1]

    if not path:
        path = ['']

    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")

        if os.path.isfile(nb_path):
            return nb_path

        nb_path = nb_path.replace("_", " ")

        if os.path.isfile(nb_path):
            return nb_path


class NotebookLoader(object):
    """This does the work of loading the code from the notebook.

    If I understand it correctly it simply goes through each cell, executing the code
    and putting the results into a Module object.
    """

    def __init__(self, path=None):
        self.shell = InteractiveShell.instance()
        self.shell.enable_gui = lambda x: False
        self.path = path

    def load_module(self, fullname):
        """Here is where the magic happens and we end up with a python module."""

        path = find_notebook(fullname, self.path)

        print("Loading code from {}".format(path))

        with io.open(path, 'r', encoding="utf-8") as f:
            nb = read(f, 4)

        # Here we do magic and create a module
        module = types.ModuleType(fullname)
        module.__file__ = path
        module.__loader__ = self
        module.__dict__['get_ipython'] = get_ipython
        sys.modules[fullname] = module

        # Further magic to enable magics to work as expected.
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = module.__dict__

        # Now we go through and execute all the cells.
        try:
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    # If the cell has magics, we need to translate into real Python.
                    src = cell.source
                    code = self.shell.input_transformer_manager.transform_cell(src)

                    exec(code, module.__dict__)
        finally:
            self.shell.user_ns = save_user_ns

        return module

class NotebookFinder(object):
    """The last piece of the puzzle and our entry point into the import system (I
    think).

    This checks to see if a path looks like a notebook, if so it returns a
    NotebookLoader to load it.
    """

    def __init__(self):
        self.loaders = {}

    def find_module(self, fullname, path=None):
        nb_path = find_notebook(fullname, path)

        if not nb_path:
            return

        key = path
        if path:
            key = os.path.sep.join(path)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)

        return self.loaders[key]

