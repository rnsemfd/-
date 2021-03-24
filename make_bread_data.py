"""
이 파일은 이미지파일들을 데이터화 시키는 파일이다.
또한 이미지를 반전시키거나 회전시켜 부족한 이미지의 갯수를 늘려주며
다양한 이미지를 만듬으로서 정밀도를 높이는 파일이다.
"""

from PIL import Image
import os, glob # 이미지 캐치를 위해
import numpy as np # numpy 이용하기 위한 import
import random, math # 랜덤함수 및 수학적 계산

root_dir = "./image/Bread3" # 이미지가 저장되어 있는 위치로 가서 가져옴
# 분류대상 카테고리 지정하기
categories = ["applepie","cream", "gorokee", "muffin",
              "pie", "pinkbread", "pizzabread", "soboro",
              "walnutpie","xbread"]
nb_classes =len(categories)
image_size = 64

X = [] # 이미지 데이터
Y = [] # 레이블 데이터 
def add_sample(cat, fname, is_train):
    img = Image.open(fname) # 이미지 데이터 열기
    img = img.convert("RGB") # 색상 모드 변환하기 
    img = img.resize((image_size, image_size)) # 이미지 크기 리사이즈 
    data = np.asarray(img) # asarray메서드로 Image 데이터를 numpy 배열데이터로 변환함  
    X.append(data) # append 기능으로 리스트에 새로 데이터 추가 
    Y.append(cat)
    if not is_train: return
    # 각도를 조금 변경한 파일 추가하기. 회전하기 
    for ang in range(-20,20,5):
        img2 = img.rotate(ang) # 회전 
        data = np.asarray(img2) # 회전한 것 numpy 배열로 변환 
        X.append(data)
        Y.append(cat)
        img2 = img2.transpose(Image.FLIP_LEFT_RIGHT) # 이미지 반전시키기 
        data = np.asarray(img2) # 반전한 것 numpy 배열로 변환 
        X.append(data)
        Y.append(cat)
    

def make_sample(files, is_train): # 학습시킬 이미지 모음들 
    global X, Y
    X = []; Y = []
    for cat, fname in files:
        add_sample(cat, fname, is_train)
    return np.array(X), np.array(Y)

allfiles = [] # 각 폴더에 들어있는 파일 수집하기
for idx, cat in enumerate(categories):
    image_dir = root_dir + "/" + cat
    files = glob.glob(image_dir + "/*.jpg")
    # glob함수를 사용하여 확장자가 jpg인것만 찾음 
    for f in files:
        allfiles.append((idx, f))

random.shuffle(allfiles) # 사진들 섞어서 랜덤으로 뽑기 
th = math.floor(len(allfiles) * 0.9) # 드롭아웃 기법으로 80%만 학습시켜 데이터가 너무 치중되지 않게끔 해둠 
train = allfiles[0:th]
test = allfiles[th:]
X_train, y_train = make_sample(train, True)
X_test, y_test = make_sample(test, False)
xy = (X_train, X_test, y_train, y_test )
np.save("breadimg5.npy", xy) # 만든 데이터셋 저장 위치 지정
print("ok,", len(y_train)) # 생성이 제대로 되었는지 확인하기 위한 생성 갯수 출력


"""
훈련 데이터와 따로 구분해둔 더미 데이터들(테스트 데이터로 표현함)을 다 같이
반전하거나 회전하여 숫자를 늘린후 섞어서 구분하면 훈련데이터와 테스트 데이터들이
같은 경우가 많이 발생하여 정답률이 굉장히 높아지는 오류가 발생 할 수 있다.
그렇기에 드롭아웃 기법을 이용하는것과 동시에 훈련 데이터만 구분하여 반전 및 회전
시켜 정밀도를 높임으로서 훈련 데이터와 나중에 테스트 할 데이터들에 차이점을 두어
성능을 향상시켰다.
"""

    
