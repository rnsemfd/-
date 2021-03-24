import sys, os
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Activation
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Dense
from keras.utils import np_utils
import numpy as np
# 케라스를 이용하기 위해, CNN기법을 위해 import 하는 것들 


root_dir = "./image/Bread3/" 
categories = ["applepie","cream", "gorokee", "muffin",
              "pie", "pinkbread", "pizzabread", "soboro",
              "walnutpie","xbread"] # 이미지 목록들 
nb_classes = len(categories)
image_size = 64


def load_dataset():
    x_train, x_test, y_train, y_test = np.load("breadimg5.npy") # 만들어둔 데이터셋을 이용할 것임 
    x_train = x_train.astype("float") / 256
    x_test = x_test.astype("float") / 256
    y_train = np_utils.to_categorical(y_train, nb_classes)
    y_test = np_utils.to_categorical(y_test, nb_classes)
    return x_train, x_test, y_train, y_test

def build_model(in_shape): # CNN 빌드 
    model = Sequential()
    model.add(Convolution2D(32, 3, 3, border_mode = 'same', input_shape= in_shape)) # 컨볼루션하고
    model.add(Activation('relu')) # 활성화 함수로 relu함수를 이용한 후
    model.add(MaxPooling2D(pool_size=(2,2))) # 풀링기법을 이용한다 
    model.add(Dropout(0.25))

    model.add(Convolution2D(64,3,3,border_mode = 'same')) # 만들어진 CNN을 더 깊게 만들기 위해 반복
    model.add(Activation('relu'))
    model.add(Convolution2D(64,3,3))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax')) # 활성화 함수 중 하나인 소프트맥스 함수
    
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    return model

def model_train(x, y):
    model = build_model(x.shape[1:])
    model.fit(x, y, batch_size=32, epochs=50) # 미니배치 사이즈 지정 및 학습 횟수(사이클)를 정한다

    return model

def model_eval(model, x, y):
    score = model.evaluate(x, y)
    print('loss=', score[0]) # 손실함수의 손실 차이를 확인하기 위해 출력 
    print('accuracy=', score[1]) # 정확도 값 확인하기 위해 출력

x_train, x_test, y_train, y_test = load_dataset()
model = model_train(x_train, y_train)
model_eval(model, x_test, y_test)

model.save("bread_modelq.h5") # 만들어진 학습데이터를 이 이름으로 저장한다
    



