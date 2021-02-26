from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from urllib import parse 

tempstorename = ' '

options = webdriver.ChromeOptions()
#options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR') 

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.implicitly_wait(5)

#driver.get('https://map.naver.com/v5/search/%EA%B0%90%EC%84%B1%ED%83%80%EC%BD%94%20/place/1306983663?c=14136846.8434011,4509216.1684275,13,0,0,0,dh&placePath=%3Fentry%253Dbmp')
driver.get('https://map.naver.com')


print("+" * 100)
print(driver.title)
print(driver.current_url)
print("-" * 100)

time.sleep(3) 


name = driver.find_element_by_xpath('//*[@id="container"]/shrinkable-layout/div/app-base/base-card/div[1]/today-weather-card/div/div[1]/a')

searchbox = driver.find_element_by_class_name('input_search')
searchbox.send_keys('내정로 165번길')
searchbox.send_keys(Keys.ENTER)

time.sleep(5) 

### 여기서부터 반복문 시작 
while True: 
   driver.switch_to.frame(driver.find_element_by_id('searchIframe'))

   #무한 스크롤 
   eula = driver.find_element_by_id('_pcmap_list_scroll_container')
   while True: 
      prev_sh = driver.execute_script('return arguments[0].scrollHeight', eula)
      driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', eula)
      time.sleep(10) 
      current_sh = driver.execute_script('return arguments[0].scrollHeight', eula)
      if prev_sh == current_sh:
         break

   stores = driver.find_elements_by_css_selector('#_pcmap_list_scroll_container > ul > li')

   time.sleep(10) 

   if stores[0].find_elements_by_tag_name('div')[1].find_element_by_tag_name('span').text == tempstorename: #마지막 페이지에 도달함 
      break 

   tempstorename = stores[0].find_elements_by_tag_name('div')[1].find_element_by_tag_name('span').text #마지막 페이지 아니면 다시 맨 처음 가게 이름 저장해놓음 

   for p in stores: 

      #개별 장소 상세 설명 클릭하기 

      p.find_elements_by_tag_name('div')[1].find_element_by_tag_name('span').click()
      time.sleep(5)

      #장소 상세 설명 창으로 가주기 
      driver.switch_to.default_content()
      driver.switch_to.frame(driver.find_element_by_id('entryIframe'))
      
      #이름, 종목명 가져오기 
      detail = driver.find_element_by_class_name('place_detail_wrapper')
      intro1 = detail.find_element_by_id('_title') #이름 + 종목명 
      intro2 = intro1.find_elements_by_tag_name('span')
      print("장소 이름: "+intro2[0].text)
      print("장소 종목명: "+intro2[1].text)

      
      #별점, 방문자 리뷰, 블로그 리뷰 가져오기 
      detail2 = driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[1]/div/div/div[1]/div')
      finalinfo = detail2.find_elements_by_tag_name('span') #'별점'이 적힌 독립적인 span 이 하나 존재한다! 

      for k in finalinfo: 
         #print(k.text)
         if k.text.find("별점") != -1 and k.text.find("/5") != -1:
            print("장소 별점: "+k.find_element_by_tag_name('em').text)
         if k.text.find("방문자리뷰") != -1:
            print("장소 방문자리뷰 수: "+k.find_element_by_tag_name('em').text)
         if k.text.find("블로그리뷰") != -1:
            print("장소 블로그리뷰 수: "+k.find_element_by_tag_name('em').text)
         if k.text.find("주문자리뷰") != -1:
            print("장소 주문자리뷰 수: "+k.find_element_by_tag_name('em').text)
      

      #주소 가져오기 
      address_list = driver.find_elements_by_tag_name('li')
      for x in address_list: 
         if x.text.find("주소") != -1:
            print("주소: "+x.find_elements_by_tag_name('span')[1].text)
            print() 
            break 


      driver.switch_to.default_content()
      driver.switch_to.frame(driver.find_element_by_id('searchIframe'))

      time.sleep(5)

   driver.find_element_by_xpath('//*[@id="app-root"]/div/div/div[2]').find_elements_by_tag_name('svg')[1].click() #'다음페이지' 클릭하는 코드 
   driver.switch_to.default_content()





