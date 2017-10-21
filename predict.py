#!/usr/local/bin/python3
# vim: set file_encoding=UTF-8:

from kerasmodel import create_model
import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt
import analysis_images as ai

if __name__ == '__main__':
    categories = ['暁美ほむら', '佐倉杏子', '鹿目まどか', '巴まみ', '美樹さやか']
    nb_classes = len(categories)

    caltech_dir = './predict-targets'
    target_images_dir = '{0}/*'.format(caltech_dir)
    target_files = glob.glob(target_images_dir)

    px = []
    files = []
    for filepath in target_files:
        image = ai.ImageConsts.openImage(filepath)
        faces = ai.ImageConsts.trimFaces(image)
        for f in faces:
            # f.show()
            files.append(filepath)
            px.append(f)


    px = np.array(ai.ImageConsts.imageArray2vectors(px))
    px = px.astype('float') / 256.

    model = create_model(ai.ImageConsts.NB_CLASSES, px.shape[1:])
    model.load_weights(filepath='./datas/keras-models.h5')
    result = model.predict(x=px, verbose=1)
    result_frame = pd.DataFrame(data=result, index=files, columns=categories)
    result_frame = result_frame.transpose()

    plt.rcParams['font.family'] = 'IPAexGothic'
    plt.style.use('ggplot')
    result_frame.plot(kind='bar', subplots=True, ylim=(0,1.1), figsize=(15, 10))
    plt.show()