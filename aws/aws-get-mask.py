import boto3
import numpy as np
import json
import requests
import click
from os import listdir
from os.path import isfile, join
import curses
from timeit import default_timer as timer
import datetime
import io

def loading(percent, message, size=20, time='', end='\r'):
  bar = '='*int(size*percent)
  space = ' '*(size - int(size*percent))
  if time != '':
    time = str(datetime.timedelta(seconds=time))
  print('[{}] {}% {} - {}{}'.format(bar+space, int(percent*100), time, message, end), end='')

def main():

  # load the configuration file
  settings = None
  try:
    with open('aws.conf', 'r') as settings:
      settings = json.load(settings)
  except Exception as e:
    print(e)
    print('Make sure your configuration file is named "aws.conf"')
    exit(2)

  s3 = boto3.client(
    's3',
    aws_access_key_id=settings['ACCESS_KEY'],
    aws_secret_access_key=settings['SECRET_KEY']
  )

  bucket = 'a.i.dermatologist'
  prefix = 'mask'

  directory_meta = '../data_procuration/data/meta'
  progress_dir   = '.progress/mask-progress.txt' 

  progress = []
  with open(progress_dir, 'r') as pf:
    for line in pf:
      progress.append(line.strip('\n'))
  onlyfiles = [f for f in listdir(directory_meta) if isfile(join(directory_meta, f)) and \
    f != '.gitkeep' and f not in progress]


  ids = {}
  for f in onlyfiles:
    with open(join(directory_meta, f), 'r') as meta:
      js = json.load(meta)
      ids[f] = js['_id']

  
  window = curses.initscr()
  window.nodelay(1)
  ch = -1

  n = len(progress) + len(onlyfiles)
  start_time = timer()

  with open(progress_dir, 'a') as pf:
    key = ''
    i = len(progress)
    for name, _id in ids.items():
      if ch > 0:
        break
      try:
        r = requests.get('https://isic-archive.com/api/v1/segmentation?limit=1&offset=0&sort=created&sortdir=-1&imageId={}'.format(_id))
        seg_id = r.json()[0]['_id']
        r = requests.get('https://isic-archive.com/api/v1/segmentation/{}/mask'.format(seg_id))
        s3.upload_fileobj(io.BytesIO(r.content),
                          bucket,
                          join(prefix, name[:-4]+'png')
        )
      except:
        pf.write(name+'\n')
        ch = window.getch()
        i += 1
        loading(i/n, name, 20, timer() - start_time)

  curses.endwin()
  loading(i/n, 'Complete', 20, timer() - start_time, end='\n')
if __name__ == '__main__':
  main()