#!/usr/local/bin/python3
import json

def main():
  # open list file containing json of metadata
  with open('./conf/list', 'r') as ifile:

    img_list = json.load(ifile)
    # iterate through each metadata item
    for item in img_list:
      # print out to stdout in csv format for download_data.sh script to read in
      print('{},{}'.format(item['name'], item['_id']))
      # store the metadata with proper name
      with open('./data/meta/{}.json'.format(item['name']), 'w') as ofile:
        json.dump(item, ofile)
        ofile.close()
    ifile.close()


if __name__ == '__main__':
  main()