#!/bin/bash

# this script will remove any data downloaded on your system

rm ./data/img/*.jpg
rm ./data/meta/*.json
rm ./data/img_mod/*.jpg
echo "" > ./conf/current_ids
echo "" > ./conf/ids
echo "" > ./conf/list