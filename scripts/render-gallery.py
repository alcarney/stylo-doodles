#!/usr/bin/env python
import sys
from pathlib import Path
from jinja2 import Template


GALLERY_TEMPLATE = "templates/index.html"
SITE_BASEURL = "/stylo-doodles"
SITE_DIR = "_site"
IMAGE_DIR = SITE_DIR + "/img"


def get_gallery_template():
    with open(GALLERY_TEMPLATE) as f:
        return Template(f.read())


def find_images(local=False):
    """Find the images and create the context needed to render the template."""

    img_dir = Path(IMAGE_DIR)
    images = []

    base_url = "" if local else SITE_BASEURL

    for image in img_dir.glob("*.png"):

        images.append({
            "url": str(image).replace("_site", base_url)
        })

    return images


def main():

    local = False

    if len(sys.argv) > 1 and sys.argv[1] == "local":
        local = True

    template = get_gallery_template()
    images = find_images(local)

    print("Found {} images.\nRendering Galery.".format(len(images)))

    gallery = template.render(images=images)

    with open(SITE_DIR + "/index.html", 'w') as f:
        f.write(gallery)


if __name__ == "__main__":
    main()



