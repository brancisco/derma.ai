import numpy as np
import json
import requests
from os import listdir
from os.path import isfile, join

def main():
  directory_meta = './data/meta'
  directory_mask = './data/img_mask'
  onlyfiles = [f for f in listdir(directory_meta) if isfile(join(directory_meta, f)) and f != '.gitkeep']
  ids = {}
  for f in onlyfiles:
    with open(join(directory_meta, f), 'r') as meta:
      js = json.load(meta)
      ids[f] = js['_id']

  count = 0
  for name, _id in ids.items():
    r = requests.get('https://isic-archive.com/api/v1/segmentation?limit=1&offset=0&sort=created&sortdir=-1&imageId={}'.format(_id))
    seg_id = r.json()[0]['_id']
    r = requests.get('https://isic-archive.com/api/v1/segmentation/{}/mask'.format(seg_id))
    with open(join(directory_mask, name[:-4]+'png'), 'wb') as out:
      out.write(r.content)
    if count > 100:
      break
    count += 1
  
  # print(onlyfiles)


if __name__ == '__main__':
  main()