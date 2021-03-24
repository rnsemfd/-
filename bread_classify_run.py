import sys, os
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
from keras.models import load_model
from PIL import Image
import os, glob
import numpy as np
import socket


image_files = glob.glob("image/testbread4/*.jpg") # 경로내의 모든 jpg파일을 가져오기

image_size = 64
nb_classes = len(image_files)
# 카테고리 분류를 통해 빵의 종류를 나눈다
categories = ["applepie","cream", "gorokee", "muffin",
              "pie", "pinkbread", "pizzabread", "soboro",
              "walnutpie","xbread"]
X = [] # 이미지 데이터
files = [] # 레이블 데이터로서 예측값이 된다 

for fname in image_files:
    img = Image.open(fname) # 이미지 데이터 열기
    img = img.convert("RGB") # 색상 모드 변환하기 
    img = img.resize((image_size, image_size)) # 이미지 크기 리사이즈
    in_data = np.asarray(img) # ararray메서드로 Image 데이터를 nunmpy 배열데이터로 변환
    in_data = in_data.astype("float") / 256
    X.append(in_data) # append 기능으로 리스트에 새로 데이터 추가 
    files.append(fname) # 예측할 데이터들 집어넣기 

X = np.array(X)

model = load_model('bread_model5.h5') # 학습한 모델 불러오기 

pre = model.predict(X) # 예측

a = [10] * 100
for i, p in enumerate(pre): # 예측한 내용 확인을 위해 반복 출력. enumerate함수를 통해 튜플 형태의 정렬 기능 추가   
    y = p.argmax() # 원 핫 인코딩 때문에 가장 큰 수를 찾기 위해 이용한다
    if p[y] < 0.95:
         print("입력:", files[i])
         print("예측값이 낮습니다.", "/ Score", p[y])
         a[i] = 10
    else:
        print("입력:", files[i])
        print("예측:", "[", y, "]", categories[y], "/ Score", p[y])
        a[i] = y
    

"""
# 서버 연결을 위해 
HOST = '220.68.231.97'
PORT =33060

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
client_socket.connect((HOST, PORT))

# 메시지를 전송합니다
j = 0
while True:
        if a[j] == 0:
           message = ('0')
           message = message+'\n'
        elif a[j] == 1:
           message = ('1')
           message = message+'\n'
        elif a[j] == 2:
           message = ('2')
           message = message+'\n'
        elif a[j] == 3:
           message = ('3')
           message = message+'\n'
        elif a[j] == 4:
           message = ('4')
           message = message+'\n'
        elif a[j] == 5:
           message = ('5')
           message = message+'\n'
        elif a[j] == 6:
           message = ('6')
           message = message+'\n'
        elif a[j] == 7:
           message = ('7')
           message = message+'\n'
        elif a[j] == 8:
           message = ('8')
           message = message+'\n'
        elif a[j] == 9:
           message = ('9')
           message = message+'\n'
        else:
           message = ('10')
           message = message+'\n'

        client_socket.send(message.encode()) 
        j = j + 1
        if j>i:
            break


# 소켓을 닫습니다.
client_socket.close()
"""



