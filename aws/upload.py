import boto3
from botocore.errorfactory import ClientError
from os.path import isdir, exists
from os import listdir
from os.path import isfile, join
import json
import sys


# --------------------------------
usage = 'python3 upload.py "name of dir in data_procuration/data/" "name of s3 folder to upload to"'
# --------------------------------
# This file should be used to upload a directory of images to an s3 bucket
# --------------------------------


def dict_val_transform(d):
  for k in d:
    d[k] = str(d[k])
  return d

def main():

  # set up the directories
  # local setup
  data_dir  = '../data_procuration/data/'
  img_dir   = sys.argv[1]
  meta_dir  = 'meta'
  # ensure directory stucture exists
  if not (exists(join(data_dir, img_dir)) and isdir(join(data_dir, img_dir))):
    print('Error:', join(data_dir, img_dir), 'does not exist')
    print('Usage:', usage)
    exit(1)

  # remote setup
  bucket_name = 'a.i.dermatologist'
  folder_name = sys.argv[2]

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

  try:
    s3.head_object(Bucket=bucket_name, Key=folder_name+'/')
  except ClientError as e:
    print(e)
    print('Usage:', usage)
    exit(3)

  u_input = input('Are you sure you want to upload the contents from {} to the s3 bucket folter {}? (y/n)\n'.\
    format(
      join(data_dir, img_dir),
      join(bucket_name, folder_name)
    )
  )
  if u_input != 'y':
    exit(4)

  # get a list of files in the 
  files = [f for f in listdir(join(data_dir, img_dir)) \
    if isfile(join(data_dir, img_dir, f)) and f != '.gitkeep']

  # iterate through local files
  for f in files:
    # open local dir containing desired images
    with open(join(data_dir, img_dir, f), 'rb') as data:
      # open dir containing corresponding metadata
      with open(join(data_dir, meta_dir, f[:-3]+'json'), 'r') as meta:
        meta = json.load(meta)
        # upload the image with metadata attached
        s3.upload_fileobj(data, 
                          bucket_name,
                          '{}/{}'.format(folder_name, f),
                          ExtraArgs={
                            'Metadata': dict_val_transform(meta['meta']['clinical'])
                          }
        )

if __name__ == '__main__':
  main()