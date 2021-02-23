from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from urllib import parse 

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

driver.switch_to.frame(driver.find_element_by_id('searchIframe'))
#stores = driver.find_element_by_id('_pcmap_list_scroll_container')
stores = driver.find_elements_by_css_selector('#_pcmap_list_scroll_container > ul > li')

for p in stores: 
   name = p.find_element_by_tag_name('span')
   name.click()

   #장소 상세 설명 창으로 가주기 
   driver.switch_to.default_content()
   driver.switch_to.frame(driver.find_element_by_id('entryIframe'))
   
   time.sleep(2)

   detail = driver.find_element_by_class_name('place_detail_wrapper')
   intro1 = detail.find_element_by_id('_title') #이름 + 종목명 
   intro2 = intro1.find_elements_by_tag_name('span')
   
   print("장소 이름: "+intro2[0].text)
   print("장소 종목명: "+intro2[1].text)

   detail2 = driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[1]/div/div/div[1]/div')
   finalinfo = detail2.find_elements_by_tag_name('em')
   print("장소 별점: "+finalinfo[0].text)
   print("장소 방문자리뷰 수: "+finalinfo[1].text)
   print("장소 블로그리뷰 수: "+finalinfo[2].text)

   time.sleep(4)

   driver.find_element_by_class_name('place_fixed_maintab').find_elements_by_tag_name('a')[0].click()

   address = driver.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('li')[1].find_elements_by_tag_name('span')[1].text
   print("장소 주소: "+address)

   #원래 프레임으로 복귀해주기 
   driver.switch_to.default_content()
   
   #print("현재 url: "+driver.current_url) 
   url = parse.urlparse(driver.current_url)

   complexcoordinate = parse.parse_qs(url.query)['c'][0]
   simplecoordinate = complexcoordinate.split(',')
   #print(simplecoordinate)

   print(float(simplecoordinate[0]))
   print(float(simplecoordinate[1]))
   print() 

   driver.switch_to.frame(driver.find_element_by_id('searchIframe'))

   time.sleep(4)
   

#driver.close()


