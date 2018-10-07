import sys
from .nb_importer import NotebookFinder

# Finally tell python about our import code.
sys.meta_path.append(NotebookFinder())

