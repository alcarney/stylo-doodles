"""This controls the main build process of the gallery site."""
import nbutils  # This does *magic* to allow us to import notebooks as modules.
import os
import shutil
import sys

from datetime import datetime
from importlib import import_module
from pathlib import Path
from tqdm import tqdm

from webutils.static import copy_static
from webutils.files import to_filename
from webutils.templates import render_template


# Site config

BASE_URL = "stylo-doodles/"

if len(sys.argv) > 1 and sys.argv[1] == "local":
    BASE_URL = "/"

GALLERY_TEMPLATE = "templates/index.html"
NB_MODULE = "notebooks"
STATIC_PATH = "static/"

SITE_PATH = "_site/"
IMG_PATH = os.path.join(SITE_PATH, "img/")
THUMBS_PATH = os.path.join(SITE_PATH, "thumbs/")


def discover_notebooks():
    """Discover and import notebook files, return a list of (info, image) pairs."""

    nbdir = Path(NB_MODULE + "/")
    notebooks = []

    for nbpath in nbdir.glob("*.ipynb"):

        pkg_name = NB_MODULE + '.' + str(nbpath.stem)
        print("Importing {}".format(pkg_name))

        nb = import_module(pkg_name)
        notebooks.append((nb.info, nb.image))

    return notebooks


def render_images(notebooks, context):
    """Render the images needed and update the context."""

    print("Rendering images...")

    if not os.path.isdir(IMG_PATH):
        os.mkdir(IMG_PATH)

    if not os.path.isdir(THUMBS_PATH):
        os.mkdir(THUMBS_PATH)

    for info, image in tqdm(notebooks):

        filename = to_filename(info['title']) + ".png"
        imgname = os.path.join(IMG_PATH, filename)
        thumbname = os.path.join(THUMBS_PATH, filename)

        # Update the info to include the filepaths
        info['urls'] = {
            "img": imgname.replace(SITE_PATH, BASE_URL),
            "thumb": thumbname.replace(SITE_PATH, BASE_URL)
        }

        width, height = info['dimensions']
        thumb_w, thumb_h = width // 4, height // 4

        image(width, height, filename=imgname)
        image(thumb_w, thumb_h, filename=thumbname)

        context['images'].append(info)



def main():

    if os.path.isdir(os.path.join('.', SITE_PATH)):
        shutil.rmtree(SITE_PATH)

    # Create the _site directory and copy static files.
    copy_static(STATIC_PATH)

    # Create context for the templates
    context = {
        "images": [],
        "last_build": datetime.now().strftime("%a %d %B %Y -- %H:%M:%S")
    }

    # Discover notebook examples to handle
    notebooks = discover_notebooks()
    render_images(notebooks, context)

    # Render the webpage
    with open(os.path.join(SITE_PATH, "index.html"), 'w') as f:
        f.write(render_template(GALLERY_TEMPLATE, context))


if __name__ == '__main__':
    main()
