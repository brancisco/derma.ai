import boto3
from botocore.errorfactory import ClientError
from os.path import isdir, exists
from os import listdir
from os.path import isfile, join
import json
import sys
import numpy as np
from timeit import default_timer as timer
import datetime


def retrieve_objects(client, bucket, prefix):
  kwargs = {
    'Bucket': bucket,
    'Prefix': prefix
  }
  keys = []
  while 1:
    res = client.list_objects_v2(**kwargs)
    keys += list(map(lambda x: x['Key'], res['Contents']))
    if 'NextContinuationToken' not in res: break
    kwargs['ContinuationToken'] = res['NextContinuationToken']

  return keys

def write_formatted_lst(keys, inds, meta_loc, lst_loc, class_map):
  out = []
  for i, k in zip(inds, keys):
    meta_key = k[:12]+'.json'
    with open(join(meta_loc, meta_key), 'r') as meta:
      meta = json.load(meta)
      out.append(
        str(i) + '\t' \
        + class_map[meta['meta']['clinical']['benign_malignant']] + '\t' \
        + k + '\n')

  
  with open(lst_loc, 'w') as lst_f:
    for l in out:
      lst_f.write(l)

def inds_gen(a, b):
  inds = list(range(a, b))
  np.random.shuffle(inds)
  for i in inds:
    yield i


class_map = {
  'benign': '0',
  'malignant': '1',
}

def main():
  bucket_name = 'a.i.dermatologist'

  prefix = str(sys.argv[1])

  data_folder = '../data_procuration/data'

  if not isdir(join(data_folder, 'lst', prefix)):
    print('create directory', join(data_folder, 'lst', prefix))

  # load the configuration file
  try:
    print('loading aws.conf file')
    settings = None
    with open('aws.conf', 'r') as settings:
      settings = json.load(settings)
  except Exception as e:
    print(e)
    print('Make sure your configuration file is named "aws.conf"')
    exit(2)

  try:
    print('creating s3 client handle')
    s3 = boto3.client(
      's3',
      aws_access_key_id=settings['ACCESS_KEY'],
      aws_secret_access_key=settings['SECRET_KEY']
    )
  except Exception as e:
    print('errror', e)

  try:
    print('downloading keys')
    keys = retrieve_objects(s3, bucket_name, prefix)
    keys = list(sorted(keys))
    keys = [k for k in keys if k[-3:] == 'jpg' or k[-3:] == 'png']
    t_keys = [k[k.find('ISIC_'):] for k in keys if k.find('train') >= 0]
    v_keys = [k[k.find('ISIC_'):] for k in keys if k.find('validation') >= 0]
  except Exception as e:
    print('error', e)
    exit()

  inds = inds_gen(0, len(keys))

  try:
    print('writing train.lst')
    write_formatted_lst(
      t_keys,
      inds,
      join(data_folder, 'meta'), 
      join(data_folder, join('lst', prefix, 'train.lst')), 
      class_map
    )
  except Exception as e:
    print('error', e)
    exit()

  try:
    print('writing validation.lst')
    write_formatted_lst(
      v_keys,
      inds,
      join(data_folder, 'meta'), 
      join(data_folder, join('lst', prefix, 'validation.lst')), 
      class_map
    )
  except Exception as e:
    print('error', e)
    exit()

  print('finished')
      

if __name__ == '__main__':
  main()