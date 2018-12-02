# derma.ai
Machine learning/vision project. The goal is to build a classifier which can predict cancerous skin lesions. Stretch: can we have the model tell us why it thinks it is cancerous.

# TODO

## script to rotate images

Reference the crop.py script for help on the format of how to work with images. Use the opencv2 lib to manipulate. For now each image should be rotated 2 extra times in a random configuration of 90 degree rotations (as long as it is not the original orientation).

The rotated images (as well as a copy of the original) should be stored in a directory called img_rot. The naming scheme should be something along the lines of:

Example:

+ Original file name: ISIC_0000001.jpg
  + Original copy file name: ISIC_0000001a.jpg
  + Random Rotation 1: ISIC_0000001b.jpg
  + Random Rotation 2: ISIC_0000001c.jpg

## script to mirror images 

Reference the crop.py script for help on the format of how to work with images. Use the opencv2 lib to manipulate. For now each image should be mirrored one time across a vertical axis down the middle of the image.

The mirrored image (as well as a copy of the original) should be stored in a directory called img_mir. The naming scheme of the files should be something along the lines of:

Example:

+ Original file name: ISIC_0000001.jpg
  + Original copy file name: ISIC_0000001a.jpg
  + Mirrored file name: ISIC_0000001b.jpg