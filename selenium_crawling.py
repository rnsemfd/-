from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

driver = webdriver.Chrome() # 구글 드라이버 사용하기
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl") # 구글 이미지 사이트로 가기
elem = driver.find_element_by_name("q") # 검색창 찾기, 소스코드에 q로 name 되어 있음
elem.clear()
keyword = "소보로" # 내가 검색할 것
elem.send_keys(keyword) # 검색창에 검색어 넣기
elem.send_keys(Keys.RETURN) # 엔터키
os.makedirs(keyword) # 폴더 생성
#driver.find_elements_by_css_selector(".rg_i.Q4LuWd")[0].click()
#time.sleep(2)
#imgUrl = (driver.find_element_by_css_selector(".n3VNCb").get_attribute("src"))
#path = 'C:/PyCharm Community Edition 2020.3/pythonProject/' + str(keyword) + '/' + "test.jpg"
#urllib.request.urlretrieve(imgUrl, path)

# 구글 페이지 스크롤을 내리기 위해
SCROLL_PAUSE_TIME = 1 # 페이지 로딩 기다리기
last_height = driver.execute_script("return document.body.scrollHeight") # 브라우저 스크롤의 길이 확인
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 스크롤 끝까지 내리기
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height: # 이전 브라우저 길이랑 비교하여 끝인지 아닌지 확인
        try:
            driver.find_element_by_css_selector(".mye4qd").click() # 이미지 더보기 버튼 누르기
        except:
            break
    last_height = new_height

# 이미지 저장하기
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd") # 이미지 클릭하기위해 요소 찾아 갯수 파악
count = 0
for image in images:
    try:
        image.click() # 이미지 클릭
        time.sleep(2)
        imgUrl = driver.find_element_by_css_selector(".n3VNCb").get_attribute("src")
        #imgUrl = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
        path = 'C:/PyCharm Community Edition 2020.3/pythonProject/' + str(keyword) + '/' + str(count) + ".jpg"
        urllib.request.urlretrieve(imgUrl, path)  # 이미지 저장
        count = count + 1
    except:
        pass

driver.close() # 종료
