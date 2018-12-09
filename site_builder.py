"""This controls the main build process of the gallery site."""
import nbutils  # This does *magic* to allow us to import notebooks as modules.
import os
import random
import shutil
import sys

from datetime import datetime
from importlib import import_module
from pathlib import Path

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from tqdm import tqdm

from webutils.static import copy_static
from webutils.files import to_filename
from webutils.templates import render_template, render_markdown


# Site config

PUBLISHED_URL = "https://alcarney.github.io"
BASE_URL = "/stylo-doodles/"

if len(sys.argv) > 1 and sys.argv[1] == "local":
    BASE_URL = "/"

GALLERY_TEMPLATE = "index.html"
IMAGE_TEMPLATE = "image.html"
PAGE_TEMPLATE = "page.html"

NB_MODULE = "notebooks"
STATIC_PATH = "static/"

SITE_PATH = "_site/"
IMG_PATH = os.path.join(SITE_PATH, "img/")
IMAGE_PATH = os.path.join(SITE_PATH, "image/")
THUMBS_PATH = os.path.join(SITE_PATH, "thumbs/")


def discover_notebooks():
    """Discover and import notebook files, return a list of (info, image) pairs."""

    nbdir = Path(NB_MODULE + "/")
    notebooks = []

    print("Loading notebooks...")

    for nbpath in nbdir.glob("*.ipynb"):

        pkg_name = NB_MODULE + "." + str(nbpath.stem)
        print("\t-> {}".format(nbpath.stem))

        nb = import_module(pkg_name)
        notebooks.append((nb.info, nb.image))

    return notebooks


def highlight_source_code(source):
    """Given python source code, highlight it."""
    return highlight(source, PythonLexer(), HtmlFormatter())


def render_page(name, text, context):
    """Render a standard page written in markdown."""

    local_context = {
        "last_build": context["last_build"],
        "baseurl": context["baseurl"],
        "page": {"content": render_markdown(text)},
    }

    with open(os.path.join(SITE_PATH, name + ".html"), "w") as f:
        f.write(render_template(PAGE_TEMPLATE, local_context))


def render_image_page(info, context):
    """Render the detailed info page for an image."""

    local_context = {
        "last_build": context["last_build"],
        "baseurl": BASE_URL,
        "info": info,
    }

    filename = to_filename(info["title"]) + ".html"

    if not os.path.isdir(IMAGE_PATH):
        os.mkdir(IMAGE_PATH)

    with open(os.path.join(IMAGE_PATH, filename), "w") as f:
        f.write(render_template(IMAGE_TEMPLATE, local_context))


def render_pages(context):
    """Render any markdown pages in /pages"""

    pagedir = Path("pages/")

    for mdfile in pagedir.glob("*.md"):

        with open(mdfile) as f:
            text = f.read()

        render_page(mdfile.stem, text, context)


def render_images(notebooks, context):
    """Render the images needed and update the context."""

    print("Rendering images...")

    if not os.path.isdir(IMG_PATH):
        os.mkdir(IMG_PATH)

    if not os.path.isdir(THUMBS_PATH):
        os.mkdir(THUMBS_PATH)

    # We want to mix things up.
    random.shuffle(notebooks)

    for info, image in tqdm(notebooks):

        name = to_filename(info["title"])
        filename = name + ".png"
        imgname = os.path.join(IMG_PATH, filename)
        thumbname = os.path.join(THUMBS_PATH, filename)

        # Update the info to include extra information for the templates
        info["filename"] = name
        info["size"] = "{0} x {1}".format(*info["dimensions"])
        info["src"] = highlight_source_code(info["src"])
        info["urls"] = {
            "img": imgname.replace(SITE_PATH, BASE_URL),
            "thumb": thumbname.replace(SITE_PATH, BASE_URL),
            "base": PUBLISHED_URL,
        }

        render_image_page(info, context)

        width, height = info["dimensions"]
        thumb_w, thumb_h = width // 4, height // 4

        image(width, height, filename=imgname)
        image(thumb_w, thumb_h, filename=thumbname)

        context["images"].append(info)


def main():

    if os.path.isdir(os.path.join(".", SITE_PATH)):
        shutil.rmtree(SITE_PATH)

    # Create the _site directory and copy static files.
    copy_static(STATIC_PATH)

    # Create context for the templates
    context = {
        "last_build": datetime.now().strftime("%d %B %Y -- %H:%M:%S"),
        "baseurl": BASE_URL,
        "images": [],
    }

    # Render any markdown pages.
    render_pages(context)

    # Discover notebook examples to handle
    notebooks = discover_notebooks()

    print("Found {} notebooks\n".format(len(notebooks)))

    render_images(notebooks, context)

    # Render the main webpage
    with open(os.path.join(SITE_PATH, "index.html"), "w") as f:
        f.write(render_template(GALLERY_TEMPLATE, context))


if __name__ == "__main__":
    main()
