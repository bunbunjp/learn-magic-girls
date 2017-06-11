#!/usr/local/bin/python3
# vim: set fileencoding=UTF-8:

from sklearn import cross_validation
from PIL import Image
import os, glob
import numpy as np

image_w, image_h = 128, 128

def image2vectors(imagefilepath):
    img = Image.open(imagefilepath)
    img = img.convert('RGB')
    img = img.resize((image_w, image_h))
    return np.asarray(img)

caltech_dir = './images'
categories = ['暁美ほむら', '佐倉杏子', '鹿目まどか', '巴まみ', '美樹さやか']
nb_classes = len(categories)
pixels = image_w * image_h

X, Y = [], []

for idx, name in enumerate(categories):
    print('idx : ', idx)
    print('name: ', name)
    label = [0 for i in range(nb_classes)]
    label[idx] = 1

    print(label)
    target_images_dir = '{0}/{1}/*'.format(caltech_dir, name)
    target_files = glob.glob(target_images_dir)
    for filepath in target_files:
        data = image2vectors(filepath)
        X.append(data)
        Y.append(label)

X = np.array(X)
Y = np.array(Y)

x_train, x_test, y_train, y_test = cross_validation.train_test_split(X, Y)
xy = (x_train, x_test, y_train, y_test)

np.save('./datas/numpy-models.npy', xy)

print(xy)