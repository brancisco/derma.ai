import cv2
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt


def main():
	dir_name_orig = './data/img'
	dir_out = './data/img_mir'
	filenames = [fn for fn in os.listdir(dir_name_orig) if fn[-3:] == 'jpg']
	
	lim = len(filenames)

	for i in range(lim):
		filename = os.path.join(dir_name_orig, filenames[i])
		img = cv2.imread(filename)
		#mirror image across y axis
		mirror_img = cv2.flip(img, +1);

		#rename files
		filenamesa = filenames[i][:12] + 'a.jpg'
		filenamesb = filenames[i][:12] + 'b.jpg'
		# print(filenames)

		#write files
		cv2.imwrite(os.path.join(dir_out, filenamesa), img)
		cv2.imwrite(os.path.join(dir_out, filenamesb), mirror_img)


if __name__ == '__main__':
  main()
