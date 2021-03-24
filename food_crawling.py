#flicker api 키 960394c14c371f0b0778c967813be547
#flicker 비밀번호: 822dc9d07bd26691


import flickrapi
import urllib
import os
from PIL import Image

# Flickr api access key
flickr = flickrapi.FlickrAPI('960394c14c371f0b0778c967813be547', '822dc9d07bd26691', cache=True)

def createFolder(keyword):
    try:
        if not os.path.exists(keyword):
            os.makedirs(keyword)
            os.makedirs('final'+keyword)
            print("create folder")
    except OSError:
        print ('Error: Creating directory. ' + keyword)


def downloadImage(keyword):
    photos = flickr.walk(text=keyword,
                         tag_mode='all',
                         tags=keyword,
                         privacy_filter=1,  # 공개된 이미지만 가져오기
                         extras='url_c',
                         per_page=100,
                         sort='relevance')

    urls = []
    num = 0
    err = 0
    for i, photo in enumerate(photos):

        url = photo.get('url_c')
        urls.append(url)

        if i + 1 > 1000:  # 가져올 이미지 갯수
            break
        if urls[i] == None:  # urls 오류가 발생시 None으로 표기되므로
            err = err + 1
        else:
            name = str(num) + ".jpg"
            num = num + 1
            path = 'C:/PyCharm Community Edition 2020.3/pythonProject/' + str(keyword) + '/' + name
            urllib.request.urlretrieve(urls[i], path)  # 가져온 이미지 주소에서 이미지를 저장함

    print("가져온 이미지 갯수: " + str(num))
    print("에러로 인한 못 가져온 이미지 갯수: " + str(err))

def main():
    keyword = '소보로'  # 가져올 사진의 이름
    createFolder(keyword)
    downloadImage(keyword)

if __name__ == "__main__":
    main()
