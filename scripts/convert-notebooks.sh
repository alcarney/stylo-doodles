#!/bin/bash

# This script goes through each notebook, executes it and converts it to
# markdown to be incorporated into the website.
if [ -d _site ]; then
    rm -r _site
fi

if [ -d build ]; then
    rm -r build
fi

# Discover the notebook files.
notebooks=$(find notebooks -name "*.ipynb")
nbcount=$(find notebooks -name "*.ipynb" | wc -l)

echo "Found $nbcount notebooks"

# For each notebook file, execute it and convert it to markdown
for nbpath in $notebooks
do
    echo -n "."
    jupyter nbconvert $nbpath --to markdown \
                              --output-dir="build" \
                              --log-level=50 \
                              --execute
done
echo

# Next find all the produced images and copy them into the _site/img folder
echo "Copying images to _site/img"
imgs=$(find build -name "*.png")
mkdir -p _site/img
mv $imgs _site/img


