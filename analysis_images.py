#!/usr/local/bin/python3
# vim: set fileencoding=UTF-8:

import cv2
import glob
import math
import os

import numpy as np
import pandas as pd
from PIL import Image


class ImageConsts:
    """画像処理系のユーティリティクラス"""
    IMAGE_WIDTH, IMAGE_HEIGHT = 64, 64
    CALTECH_DIR = './images'
    DUMMY_DATA_PATH = './bulk-images'
    CATEGORIES = ['暁美ほむら', '佐倉杏子', '鹿目まどか', '巴まみ', '美樹さやか']
    NB_CLASSES = len(CATEGORIES)
    PIXELS = IMAGE_WIDTH * IMAGE_HEIGHT
    FACE_CASCADE = cv2.CascadeClassifier('lbpcascade_animeface/lbpcascade_animeface.xml')

    @staticmethod
    def trimFaces(imagePil):
        """
        顔抽出メソッド
        :param imagePil:
        :return faceImages: 抽出した顔データ配列
        """
        image = np.array(imagePil, 'uint8')
        faceImages = []
        faces = ImageConsts.FACE_CASCADE.detectMultiScale(image)
        for (x, y, w, h) in faces:
            resizedImage = cv2.resize(image[y: y + h, x: x + w], (ImageConsts.IMAGE_WIDTH, ImageConsts.IMAGE_HEIGHT), interpolation=cv2.INTER_LINEAR)
            faceImages.append(Image.fromarray(resizedImage))
        return faceImages

    @staticmethod
    def nbClasses2categoryName(nb):
        """
        カテゴリベクトルをキャラ名に変換します
        :param nb:
        :return charname: キャラクタ名
        """
        idx = -1
        for i in range(0, len(ImageConsts.CATEGORIES)):
            if nb[i] == 1:
                idx = i
        return ImageConsts.CATEGORIES[idx]

    @staticmethod
    def imageArray2vectors(images):
        """
        画像を画像ベクトルに変換します
        :param images:
        :return result: 変換されたベクトル配列
        """
        result = []
        for img in images:
            img = img.resize((ImageConsts.IMAGE_WIDTH, ImageConsts.IMAGE_HEIGHT))
            nparray = np.asarray(img).astype('float')
            result.append(nparray)
        return result

    @staticmethod
    def openImage(imagefilepath):
        """
        画像ファイルを開いてRGBデータにコンバートします
        :param imagefilepath:
        :return img: RGBイメージ
        """
        img = Image.open(imagefilepath)
        img = img.convert('RGB')
        return img


    @staticmethod
    def bulkingTrainingData(x_train, y_train):
        """
        学習用データを水増しします
        :param x_train:
        :param y_train:
        :return (x_train, y_train): 水増しした学習データ
        """
        x_result, y_result = [], []

        for idx in range(0, len(x_train)):
            image = x_train[idx]
            labelIdx = y_train[idx]
            charName = ImageConsts.nbClasses2categoryName(labelIdx)
            charDirPath = '{0}/{1}'.format(ImageConsts.DUMMY_DATA_PATH, charName)
            counter = 0

            if not os.path.exists(charDirPath):
                os.mkdir(charDirPath)

            imageName = '{0}/{1}-{2}.jpg'.format(charDirPath, idx, counter)
            print('imageName is ', np.array(image).astype('float').mean())
            image.save(imageName)
            counter += 1

            x_result.append(image)
            y_result.append(labelIdx)

            for ang in range(-20, 20, 5):
                rotateImage = image.rotate(ang)
                rotateImage = rotateImage.convert('RGB')
                print('rotateImage is ', np.array(rotateImage).astype('float').mean())
                rotateImage.save('{0}/{1}-{2}.jpg'.format(charDirPath, idx, counter))  # charDirPath + '/' + labelIdx + '-' + counter + '.jpg'

                x_result.append(rotateImage)
                y_result.append(labelIdx)

                counter += 1

            flipImage = image.transpose(Image.FLIP_LEFT_RIGHT)
            print('flipImage is ', np.array(flipImage).astype('float').mean())
            flipImage.save('{0}/{1}-{2}.jpg'.format(charDirPath, idx, counter))

            x_result.append(flipImage)
            y_result.append(labelIdx)
            counter += 1

        return (x_result, y_result)

if __name__ == '__main__':

    # 学習データの水増し処理
    train = []
    for idx, name in enumerate(ImageConsts.CATEGORIES):
        print('idx : ', idx)
        # print('name: ', name)
        label = [0 for i in range(ImageConsts.NB_CLASSES)]
        label[idx] = 1

        print(label)
        target_images_dir = '{0}/{1}/*'.format(ImageConsts.CALTECH_DIR, name)
        target_files = glob.glob(target_images_dir)
        for filepath in target_files:
            data = ImageConsts.openImage(filepath)
            faces = ImageConsts.trimFaces(data)
            for f in faces:
                train.append({'image': f, 'label': label})

    train = pd.DataFrame(data=train)
    train = train.reindex(np.random.permutation(train.index)).reset_index(drop=True)

    th = math.floor(len(train) * 0.8)
    x_train, y_train = ImageConsts.bulkingTrainingData(train['image'][0:th], train['label'][0:th])
    x_test, y_test = (train['image'][th:].tolist(), train['label'][th:].tolist())

    xy = (x_train, x_test, y_train, y_test)
    xy = np.array(xy)

    np.save('./datas/numpy-models.npy', xy)

    print("done.")
