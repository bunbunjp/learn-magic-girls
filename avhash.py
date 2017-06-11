#!/usr/local/bin/python3
# vim: set fileencoding=UTF-8:

from PIL import Image
import numpy as np

def average_hash(file_name, size=16):
    img = Image.open(file_name)
    img = img.convert('L')
    img = img.resize(size=(size, size), resample=Image.ANTIALIAS)
    pixel_data = img.getdata()
    pixels = np.array(pixel_data)
    pixels = np.reshape(pixels, (size, size))
    avg = pixels.mean()
    diff = 1 * (pixels > avg)
    return diff


def np2hash(ahash):
    bhash = []
    for nl in ahash.tolist():
        s1 = [str(i) for i in nl]
        s2 = ''.join(s1)
        i = int(s2, 2)
        bhash.append('%04x' % i)
    return ''.join(bhash)


while True:
    filename = input('ファイル名: ')
    avg_hash = average_hash(file_name='images/{0}'.format(filename))
    print(avg_hash)
    print(np2hash(avg_hash))
