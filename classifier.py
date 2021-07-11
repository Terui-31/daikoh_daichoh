from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Flatten, Dense
from tensorflow.keras import optimizers
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf


def resnet(image_data):

    """
    画像を受け取りラベル（工種）を返す分類器
    """

    classes = ['土工事', '鉄筋工事', 'コンクリート工事', '鉄骨工事', '屋根工事',  '塗装工事', '舗装工事']
    nb_classes = len(classes) # softmaxで扱うクラス数
    img_width, img_height = 224, 224

    input_tensor = Input(shape=(img_width, img_height, 3))
    resnet50 = ResNet50(include_top=False, 
                        weights='imagenet', 
                        input_tensor=input_tensor
                        )
    top_model = Sequential()
    top_model.add(Flatten(input_shape=resnet50.output_shape[1:]))
    top_model.add(Dense(nb_classes, activation='softmax'))

    model = Model(inputs=resnet50.input, outputs=top_model(resnet50.output))

    #model.load_weights("./weights/classifier_weight.hdf5") # ファインチューニングした重みを読み込む
    model.load_weights("./weights/classifier_weight_ver07-02.h5")

    #image_data = './test/*.jpg'
    img = image.load_img(image_data, target_size=(img_width, img_height)) # 引数の画像を受けモデルに流す
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255
    pred = model.predict(x)[0] # 予測

    # 最も自信のあるラベルを受け取る
    top_label = classes[pred.argmax()]

    return top_label