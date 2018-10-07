#!/bin/bash

./scripts/convert-notebooks.sh
python scripts/render-gallery.py $1
./scripts/copy-static.sh
