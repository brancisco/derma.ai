#!/bin/bash

# this script will remove any data downloaded on your system

rm ./data/img/*.jpg
rm ./data/meta/*.json
rm ./data/img_mod/*.jpg
rm ./data/img_crop/*.png
rm ./data/img_rot/*.jpg
rm ./data/img_mir/*.jpg
rm ./data/img_mask/*.png
echo "" > ./conf/current_ids
echo "" > ./conf/ids
echo "" > ./conf/list