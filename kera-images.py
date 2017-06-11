#!/usr/local/bin/python3
# vim: set fileencoding=UTF-8:

from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import numpy as np

categories = ['暁美ほむら', '佐倉杏子', '鹿目まどか', '巴まみ', '美樹さやか']
nb_classes = len(categories)

image_w, image_h = 128, 128

x_train, x_test, y_train, y_test = np.load('./datas/numpy-models.npy')

x_train = x_train.astype('float') / 256
x_test  = x_test.astype('float') / 256


model = Sequential()
model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Convolution2D(64, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(Convolution2D(64, 3, 3))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=32, nb_epoch=50)
model.save_weights(filepath='./datas/keras-models.h5', overwrite=True)

score = model.evaluate(x_test, y_test)
print('loss=', score[0])
print('accuracy=', score[1])