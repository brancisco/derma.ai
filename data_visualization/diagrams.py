import os
import json
import pandas as pd
import csv
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# import data
path_to_json = './meta/'
json_files = [pos_json for pos_json in os.listdir( path_to_json) if pos_json.endswith('.json')]


# store data
data = []
for filename in json_files:
  with open('{}{}'.format(path_to_json, filename)) as f:
        data.append(json.load(f))


# Counting # benign and # malignant
print ("Configuring benign vs malignant")
bm = []
labels = []
values = []
for d in data:
  if 'benign_malignant' in d['meta']['clinical']:
	  bm.append(d['meta']['clinical']['benign_malignant'])

bmd = Counter(bm)
for key, val in sorted(bmd.items(), key=lambda x: x[1], reverse=True):
  if key == None:
    labels.append('none')
  else:
    labels.append(key)
  
  print("Benign/Malignant: ", key, "Count:", val)
  values.append(val)

num_bins = 5
plt.bar(labels[:2], values[:2])
plt.show()

print ("----------------------------------------")

# count diagnosis
print ("Configuring Diagnosis")
l = []
labels = []
values = []
for d in data:
  if 'diagnosis' in d['meta']['unstructured']:
	  l.append(d['meta']['unstructured']['diagnosis'])

lc = Counter(l)
for key, val in sorted(lc.items(), key=lambda x: x[1], reverse=True):
  if val > 3:
    labels.append(key)
    values.append(val)
  print("Diagnosis: ", key, "Count:", val)

plt.xticks(rotation=90, fontsize=10)
plt.yscale('log')
plt.title("Diagnosis")
plt.ylabel("Frequency")
plt.bar(labels, values)
plt.show()
print ("----------------------------------------")

# count ages
a = []
labels = []
values = []
for d in data:
  if 'age_approx' in d['meta']['clinical']:
	  a.append(d['meta']['clinical']['age_approx'])

ad = Counter(a)
for key, val in sorted(ad.items(), key=lambda x: x[1], reverse=True):
	# print("Age: ", key, "Count:", val)
  if key != None:
    labels.append(key)
    values.append(val)

plt.yscale('log')
plt.title("Age")
plt.ylabel("Frequency")
plt.bar(labels, values)
plt.show()