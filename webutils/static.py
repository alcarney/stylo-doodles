"""Utilities for working with static files."""
from shutil import copytree


def copy_static(src):
    """Copy the given folder into the _site/ directory"""
    copytree(src, "_site/")
