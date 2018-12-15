import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from os.path import join

def main():
 
  dir_name = 'data/img/'
  mask_dir = 'data/img_mask/'
  filenames = list(sorted([fn for fn in os.listdir(dir_name) if fn[-3:] == 'jpg']))
  # set preview to true if you just want tot view the images instead of write
  preview = False
  # change increment to change how many images to write out or view
  incr  = 10
  # change offset of where to start in dataset
  offset = 0
  total = offset+incr # len(filenames)
  for i in range(offset, total):
    im_id = i
    filename = join(dir_name, filenames[i])
    img = cv2.imread(filename)
    imgc = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgc = cv2.cvtColor(imgc, cv2.COLOR_BGR2RGB)
    imgg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, imgb = cv2.threshold(imgg, 130, 255, 1)
    # imgb = cv2.adaptiveThreshold(imgg, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(imgb, kernel, iterations = 5)
    dilation = cv2.dilate(erosion, kernel, iterations = 20)

    final = cv2.bitwise_and(img, img, mask=dilation)

    _, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
      imgc = cv2.drawContours(imgc, [c], 0, (0, 255, 0), 5)

    imgcb = img.copy()
    x,y,w,h = cv2.boundingRect(contours[np.argmax(list(map(len, contours)))])
    cv2.rectangle(imgcb,(x,y),(x+w,y+h),(255,0,0), 10)

    imgcbs = imgcb.copy()
    # this is necessary to create squares instead of rect
    # ------------------------------------
    # add a little bit of background
    increase_by = 30
    # make sure the width is not bigger than bounds of image
    if w + increase_by < img.shape[1]:
      # shift left
      x -= int(increase_by/2)
      # increase width
      w += increase_by
    else:
      x = 0
      w = img.shape[1]

    # make sure the height is not bigger than bounds of image
    if h + increase_by < img.shape[0]:
      # shift up
      y -= int(increase_by/2)
      # increase width
      h += increase_by
    else:
      y = 0
      h = img.shape[0]
    
    # make sure square dimensions
    if w > h and w < img.shape[0]:
      # shift up by half the difference in width and height
      y -= int(abs(w-h)/2)
      # set height to width
      h = w
    elif h > w and h < img.shape[1]:
      # shift up by half the difference in the height and the width
      x -= int(abs(h-w)/2)
      # set width to height
      w = h
    elif w < h:
      # shift up by half the difference in width and height
      y += int(abs(w-h)/2)
      # set height to width
      h = w
    elif h < w:
      # shift up by half the difference in the height and the width
      x += int(abs(h-w)/2)
      # set width to height
      w = h

    # ensure y and x havent gone negative (img will be just slightly off centered.. this is fine)
    y = max(0, y)
    x = max(0, x)

    cv2.rectangle(imgcbs,(x,y),(x+w,y+h),(0,0,255), 10)

    images = [img, imgg, imgb, erosion, dilation, final, imgc, imgcb, imgcbs]
    cmaps  = ['viridis', 'gray', 'gray', 'gray','gray', 'viridis', 'viridis', 'viridis', 'viridis']
    for ii in range(1, len(images)+1):
      plt.subplot(3, 3, ii), plt.imshow(images[ii-1], cmap=cmaps[ii-1])
    if preview:
      plt.show()
    else:
      cv2.imwrite(join(mask_dir, filenames[i]), dilation)


if __name__ == '__main__':
  main()