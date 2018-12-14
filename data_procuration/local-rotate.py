import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import random


def main():

  dir_name_orig = './data/img'
  dir_out = './data/img_rot'
  filenames = [fn for fn in os.listdir(dir_name_orig) if fn[-3:] == 'jpg']

  # print(filenames)

  lim = len(filenames)
  
  for i in range(lim):
    filename = os.path.join(dir_name_orig, filenames[i])
    img = cv2.imread(filename)
    img_orig = cv2.imread(filename) 
    
    # rotation
    num_rows, num_cols = img.shape[:2]
    rotation_matrix1, rotation_matrix2 = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), 180, 1), cv2.getRotationMatrix2D((num_cols/2, num_rows/2), 270, 1)
    img_rotation1, img_rotation2 = cv2.warpAffine(img, rotation_matrix1, (num_cols, num_rows)), cv2.warpAffine(img, rotation_matrix2, (num_cols, num_rows))

    # file names
    filenamea, filenameb = filenames[i][:12] + 'a.jpg', filenames[i][:12] + 'b.jpg'
    filenamec = filenames[i][:12] + 'c.jpg'


    cv2.imwrite(os.path.join(dir_out, filenamea), img_orig)
    cv2.imwrite(os.path.join(dir_out, filenameb), img_rotation1)
    cv2.imwrite(os.path.join(dir_out, filenamec), img_rotation2)

if __name__ == '__main__':
  main()