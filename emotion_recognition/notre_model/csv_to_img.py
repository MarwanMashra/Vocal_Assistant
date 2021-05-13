import numpy as np
import pandas as pd
import os
from PIL import Image

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

df = pd.read_csv('data/fer2013.csv')

    
df0 = df[df['emotion'] == 0]
df1 = df[df['emotion'] == 1]
df2 = df[df['emotion'] == 2]
df3 = df[df['emotion'] == 3]
df4 = df[df['emotion'] == 4]
df5 = df[df['emotion'] == 5]
df6 = df[df['emotion'] == 6]

ensure_dir("data/validation/")
ensure_dir("data/validation/Angry/")
ensure_dir("data/validation/Disgusted/")
ensure_dir("data/validation/Fearful/")
ensure_dir("data/validation/Happy/")
ensure_dir("data/validation/Sad/")
ensure_dir("data/validation/Surprised/")
ensure_dir("data/validation/Neutral/")

d=0
for image_pixels in df0.iloc[1:,1]:
    image_string = image_pixels.split(' ')
    image_data = np.asarray(image_string, dtype=np.uint8).reshape(48,48)
    img = Image.fromarray(image_data)
    img.save("data/validation/Angry/img_%d.jpg"%d, "JPEG")
    d+=1

d=0
for image_pixels in df1.iloc[1:,1]:
    image_string = image_pixels.split(' ')
    image_data = np.asarray(image_string, dtype=np.uint8).reshape(48,48)
    img = Image.fromarray(image_data)
    img.save("data/validation/Disgusted/img_%d.jpg"%d, "JPEG")
    d+=1

d=0
for image_pixels in df2.iloc[1:,1]:
    image_string = image_pixels.split(' ')
    image_data = np.asarray(image_string, dtype=np.uint8).reshape(48,48)
    img = Image.fromarray(image_data)
    img.save("data/validation/Fearful/img_%d.jpg"%d, "JPEG")
    d+=1

d=0
for image_pixels in df3.iloc[1:,1]:
    image_string = image_pixels.split(' ')
    image_data = np.asarray(image_string, dtype=np.uint8).reshape(48,48)
    img = Image.fromarray(image_data)
    img.save("data/validation/Happy/img_%d.jpg"%d, "JPEG")
    d+=1

d=0
for image_pixels in df4.iloc[1:,1]:
    image_string = image_pixels.split(' ')
    image_data = np.asarray(image_string, dtype=np.uint8).reshape(48,48)
    img = Image.fromarray(image_data)
    img.save("data/validation/Sad/img_%d.jpg"%d, "JPEG")
    d+=1

d=0
for image_pixels in df5.iloc[1:,1]:
    image_string = image_pixels.split(' ')
    image_data = np.asarray(image_string, dtype=np.uint8).reshape(48,48)
    img = Image.fromarray(image_data)
    img.save("data/validation/Surprised/img_%d.jpg"%d, "JPEG")
    d+=1

d=0
for image_pixels in df6.iloc[1:,1]:
    image_string = image_pixels.split(' ')
    image_data = np.asarray(image_string, dtype=np.uint8).reshape(48,48)
    img = Image.fromarray(image_data)
    img.save("data/validation/Neutral/img_%d.jpg"%d, "JPEG")
    d+=1