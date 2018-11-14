
# this script will push data on our aws s3 bucket mofo
import boto3
from os import path
import glob

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Get file paths
names_path = []
for name in glob.glob('../data_procuration/data/img/ISIC_*.jpg'):
    names_path.append(name)


# Upload a new file
for img in names_path:
    data = open(img, 'rb')
    key = img[29:]

    s3.Bucket('a.i.dermatologist').put_object(
        Key='unmodifiedData/' + key, Body=open(img, 'rb'))
