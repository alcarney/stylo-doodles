"""This controls the main build process of the gallery site."""
import nbutils  # This does *magic* to allow us to import notebooks as modules.

from nbutils.nb_info import import_notebook


info, image = import_notebook("notebooks.jack_o_lantern")
print(info, image)
