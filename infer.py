import pickle
import os
import tracemalloc

from skimage.io import imread
from skimage.transform import resize

tracemalloc.start()


with open('./SVCModel1.p', 'rb') as f:
    model = pickle.load(f)

image_path = './PlantVillage/Tomato__Tomato_YellowLeaf__Curl_Virus/00a538f3-8421-43ab-9e6f-758d36180dd3___YLCV_NREC 2667.JPG'

img = imread(image_path)
img = resize(img, (15, 15)).flatten()

pred = model.predict([img])

print(pred)

current, peak = tracemalloc.get_traced_memory()

print(f"Current memory usage: {current / 10**6:.2f} MB")
print(f"Peak memory usage:    {peak / 10**6:.2f} MB")

# Stop tracking
tracemalloc.stop()