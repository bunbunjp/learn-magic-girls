#!/usr/local/bin/python3
# vim: set file_encoding=UTF-8:

import numpy as np

import analysis_images as ai
from kerasmodel import create_model


if __name__ == '__main__':
    x_train, x_test, y_train, y_test = np.load('./datas/numpy-models.npy')

    x_train = np.array(ai.ImageConsts.imageArray2vectors(x_train))
    x_test = np.array(ai.ImageConsts.imageArray2vectors(x_test))

    y_train = np.array(y_train)
    y_test = np.array(y_test)

    x_train = x_train.astype('float') / 256.
    x_test = x_test.astype('float') / 256.  # 256色

    model = create_model(ai.ImageConsts.NB_CLASSES, x_train.shape[1:])
    model.fit(x=x_train, y=y_train, batch_size=32, epochs=30)
    model.save_weights(filepath='./datas/keras-models.h5', overwrite=True)

    score = model.evaluate(x_test, y_test)
    print('loss=', score[0])
    print('accuracy=', score[1])

