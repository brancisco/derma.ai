import numpy as np
import cv2
import matplotlib.pyplot as plt
import os


def main():
 
  dir_name = './data/img_mask'
  dir_name_orig = './data/img'
  dir_out = './data/img_crop'
  filenames = [fn for fn in os.listdir(dir_name) if fn[-3:] == 'png']

  for i in range(len(filenames)):
    filename = os.path.join(dir_name, filenames[i])
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
      img = cv2.drawContours(img, [c], 0, (0, 255, 0), 5)

    x,y,w,h = cv2.boundingRect(contours[np.argmax(list(map(len, contours)))])
    # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0), 10)

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

    print('{}: w,h({}, {}), x,y({}, {})'.format(filenames[i], w, h, x, y))
    img = img[y:y+h, x:x+w]
    img_orig = cv2.imread(os.path.join(dir_name_orig, filenames[i][:-3]+'jpg'))
    img_orig = img_orig[y:y+h, x:x+w]
    cv2.imwrite(os.path.join(dir_out, filenames[i]), img_orig)


if __name__ == '__main__':
  main()