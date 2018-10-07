#!/bin/bash

echo "Copying static files"
cp -r static/* _site/
touch _site/.nojekyll
