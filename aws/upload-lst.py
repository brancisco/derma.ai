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

def main():
  bucket_name = 'a.i.dermatologist'
  prefix = sys.argv[1]

  data_folder = '../data_procuration/data'

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

  n_train = 0
  n_test  = 0
  with open(join(data_folder, 'lst', prefix, 'train.lst')) as f:
    for _ in f:
      n_train += 1
  with open(join(data_folder, 'lst', prefix, 'validation.lst')) as f:
    for _ in f:
      n_test += 1

  print('n train: ', n_train)
  print('n test: ', n_test)
  print('test size: {}%'.format(n_test/(n_train+n_test)))
  if input('do these sizes match with what you would expect? (y/n)\n') != 'y':
    exit()


  try:
    print('creating s3 client handle')
    s3 = boto3.client(
      's3',
      aws_access_key_id=settings['ACCESS_KEY'],
      aws_secret_access_key=settings['SECRET_KEY']
    )
  except Exception as e:
    print(e)

  for out_f in ['train.lst', 'validation.lst']:
    try:
      print('uploading', out_f)
      s3.upload_file(join(data_folder, 'lst', prefix, out_f), bucket_name, join(prefix, out_f))
    except Exception as e: 
      print('error on', out_f, 'file: ', e)
      exit()

if __name__ == '__main__':
  main()