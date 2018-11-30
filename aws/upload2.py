import boto3
from os import listdir
from os.path import isfile, join
import json

def dict_val_transform(d):
  for k in d:
    d[k] = str(d[k])
  return d

def main():

  data_dir  = '../data_procuration/data/'
  img_dir   = 'img'
  meta_dir  = 'meta'
  s3 = boto3.client('s3')

  files = [f for f in listdir(join(data_dir, img_dir)) \
    if isfile(join(data_dir, img_dir, f)) and f != '.gitkeep']

  for f in files:
    with open(join(data_dir, img_dir, f), 'rb') as data:
      with open(join(data_dir, meta_dir, f[:-3]+'json'), 'r') as meta:
        meta = json.load(meta)
        s3.upload_fileobj(data, 
                          'a.i.dermatologist',
                          'unmodifiedData/{}'.format(f),
                          ExtraArgs={
                            'Metadata': dict_val_transform(meta['meta']['clinical'])
                          }
        )

if __name__ == '__main__':
  main()