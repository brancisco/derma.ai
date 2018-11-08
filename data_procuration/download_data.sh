#!/bin/bash

# script to download data from https://isic-archive.com/api/v1

# read in the offset
offset="$(wc -l ./conf/ids | awk '{print $1}')"
# how much data to download
chunk="50"

# curl list from isic api from [offset : offset + chunk]
curl -X GET --header 'Accept: application/json' "https://isic-archive.com/api/v1/image?limit=$(echo $chunk)&offset=$(echo $offset)&sort=name&sortdir=1&detail=true" -o './conf/list'

# get ids from the json returned from curl
python3 ./get_meta.py > ./conf/current_ids

# add curernt ids to file containing list of ongoing ids for bookkeeping purposes (offset)
cat ./conf/current_ids >> ./conf/ids

for name_id in $(cat ./conf/current_ids); do
  img_name="$(echo $name_id | awk '{split($1, a, ","); print a[1]}')"
  _id="$(echo $name_id | awk '{split($1, a, ","); print a[2]}')"

  curl -X GET --header 'Accept: application/jpg' "https://isic-archive.com/api/v1/image/$(echo $_id)/download" -o "./data/img/$(echo $img_name).jpg"
done
