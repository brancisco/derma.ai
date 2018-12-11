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


# --------------------------------
usage = 'Usage: python3 upload.py float(split_size) "name of dir in data_procuration/data/" "name of s3 folder to upload to"'
# --------------------------------
# This file should be used to upload a directory of images to an s3 bucket
# --------------------------------

def loading(percent, message, size=20, time=''):
  bar = '='*int(size*percent)
  space = ' '*(size - int(size*percent))
  if time != '':
    time = str(datetime.timedelta(seconds=time))
  print('[{}] {}% {} - {}\r'.format(bar+space, int(percent*100), time, message), end='')

def dict_val_transform(d):
  for k in d:
    d[k] = str(d[k])
  return d

class_map = {
  'benign': '0',
  'malignant': '1',
}

def main():
  try:
    test_split = float(sys.argv[1])
  except:
    print(usage)

  # set up the directories
  # local setup
  data_dir  = '../data_procuration/data/'
  img_dir   = sys.argv[2]
  meta_dir  = 'meta'
  # ensure directory stucture exists
  if not (exists(join(data_dir, img_dir)) and isdir(join(data_dir, img_dir))):
    print('Error:', join(data_dir, img_dir), 'does not exist')
    print(usage)
    exit(1)

  # remote setup
  bucket_name = 'a.i.dermatologist'
  folder_name = sys.argv[3]

  # load the configuration file
  settings = None
  try:
    with open('aws.conf', 'r') as settings:
      settings = json.load(settings)
  except Exception as e:
    print(e)
    print('Make sure your configuration file is named "aws.conf"')
    exit(2)

  # create s3 client handle
  s3 = boto3.client(
    's3',
    aws_access_key_id=settings['ACCESS_KEY'],
    aws_secret_access_key=settings['SECRET_KEY']
  )

  # try:
  #   s3.head_object(Bucket=bucket_name, Key=folder_name+'/')
  # except ClientError as e:
  #   print(e)
  #   u_input = input('No key in "{}" named "{}". Would you like to create key?(y/n)\n'.format(
  #     bucket_name, folder_name
  #   ))
  #   if u_input != 'y':
  #     print(usage)
  #     exit(3)

  u_input = input('Are you sure you want to upload the contents from "{}" to the s3 bucket folter "{}"? (y/n)\n'.\
    format(
      join(data_dir, img_dir),
      join(bucket_name, folder_name)
    )
  )
  if u_input != 'y':
    exit(4)

  # clear the .lst files
  with open(join(data_dir, 'lst/train.lst'), 'w') as t_lst_file:
    pass
  with open(join(data_dir, 'lst/validation.lst'), 'w') as v_lst_file:
    pass

  # get a list of files in the 
  files = [ f for f in\
   listdir(join(data_dir, img_dir))\
   if isfile(join(data_dir, img_dir, f)) and f != '.gitkeep']

  # shuffle to ensure data from different datasets are in train and validation
  np.random.shuffle(files)

  # limit # of uploads
  if 'RESTRICT' in settings and settings['RESTRICT'] != 0:
    files = files[:int(settings['RESTRICT'])]

  n_files = len(files)

  f_range = list(range(n_files))
  np.random.shuffle(f_range)

  files = list(zip(f_range, files))
  n_in_train = int(n_files*(1 - test_split))
  start_time = timer()
  # iterate through local files
  for i, f in zip(range(len(files)), files):
    # open local dir containing desired images
    with open(join(data_dir, img_dir, f[1]), 'rb') as data:
      # open dir containing corresponding metadata
      with open(join(data_dir, meta_dir, f[1][:-3]+'json'), 'r') as meta:
        meta = json.load(meta)
        if i < n_in_train:
          train_or_validation = 'train'
        else:
          train_or_validation = 'validation'
        # upload the image with metadata attached
        loading(i/n_files, f[1], time=(timer() - start_time))
        if 'benign_malignant' not in meta['meta']['clinical'] or \
         not (str(meta['meta']['clinical']['benign_malignant']).lower() == 'benign' or \
         str(meta['meta']['clinical']['benign_malignant']).lower() == 'malignant'):
          continue
        # s3_key = '{}/{}/{}/{}'.format(
        #                     folder_name,
        #                     train_or_validation,
        #                     meta['meta']['clinical']['benign_malignant'],
        #                     f[1]
        # )
        s3_key = '{}/{}/{}'.format(
                            folder_name,
                            train_or_validation,
                            f[1]
        )
        s3.upload_fileobj(data,
                          bucket_name,
                          s3_key,
                          ExtraArgs={
                            'Metadata': dict_val_transform(meta['meta']['clinical'])
                          }
        )
        if train_or_validation == 'train':
          with open(join(data_dir, 'lst/train.lst'), 'a') as t_lst_file:
            t_lst_file.write(str(f[0]) + '\t' +\
             class_map[meta['meta']['clinical']['benign_malignant']] + '\t' +\
             f[1] + '\n')
        else:
          with open(join(data_dir, 'lst/validation.lst'), 'a') as v_lst_file:
            v_lst_file.write(str(f[0]) + '\t' +\
             class_map[meta['meta']['clinical']['benign_malignant']] + '\t' +\
             f[1] + '\n')

  s3.upload_file(join(data_dir, 'lst/train.lst'), bucket_name, join(folder_name, 'train.lst'))
  s3.upload_file(join(data_dir, 'lst/validation.lst'), bucket_name, join(folder_name, 'validation.lst'))

  print('\n')
  print('Time For Execution: ', str(datetime.timedelta(seconds=timer() - start_time)))

if __name__ == '__main__':
  main()