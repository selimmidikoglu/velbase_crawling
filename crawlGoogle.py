from selenium import webdriver
import sys
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
#from configDataBase import connectToDB
from selenium.common.exceptions import TimeoutException
import requests
import re


username = "intenwin"
password = "42e7c5-889eb2-964986-465bf4-9acc5e"

PROXY_RACK_DNS = "megaproxy.rotating.proxyrack.net:222"

urlToGet = "http://ip-api.com/json"

proxy = {"http": "http://{}:{}@{}".format(username, password, PROXY_RACK_DNS)}
proxy = 'http://intenwin:42e7c5-889eb2-964986-465bf4-9acc5e@megaproxy.rotating.proxyrack.net:222'
#r = requests.get(urlToGet)

# print("Response:\n{}".format(r.text))
chrome_options = webdriver.ChromeOptions()

# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--window-size=1920x1080")  # I added this
chrome_options.add_argument("--ignore-certificates-errors")


desired_caps = chrome_options.to_capabilities()
# Create proxy
'''prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = proxy
prox.socks_proxy = proxy
prox.ssl_proxy = proxy
prox.add_to_capabilities(desired_caps)'''


mainUrl = "http://www.google.com/search?q="
dataDic = {
    "name": "",
    "website": "",
    "price_range": "",
    "category": "",
    "phone": "",
    "review_count": ""

}


# print(row)
#urlStr = mainUrl + row[0].replace(" ", "+") + "+" + row[1].replace(" ","+") + "+" + row[2]
#urlStr = mainUrl + "burger+king+los+angeles+ca" + "&lr=lang_en"
urlStr = 'http://www.google.com/search?q=Health+Dept+Sulphur+Springs+TX&lr=lang_en'
print(urlStr)
#PROXY = "209.205.212.34:1213"
#chrome_options.add_argument('--proxy-server=%s' % proxy)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(urlStr)
try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cXedhc,div.fYOrjf")))
    print(len(element))
    # sys.exit()
    '''if element is None:
        print('not none')
    else:
        sys.exit()'''
    # There is only one data
    if(len(element) == 1):
        element1 = driver.find_element_by_class_name('vk_bk').click
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', class_='xpdopen')
        # BUSINESS NAME
        print("NAME")
        header = soup.find_all('div', class_='kno-ecr-pt')
        headerText = header[0].find_all('span')
        print("NAME => " + headerText[0].text)
        # WEBSITE
        # print("WEBSITE")
        website_direction = soup.find_all('div', class_='QqG1Sd')
        if(len(website_direction) != 0):
            websiteDiv = website_direction[0].find('a', href=True)
            print("WEBSITE => " + websiteDiv['href'])
        else:
            print("There is no website")

        # DIRECTIONS
        direction = website_direction[1].find('a', href=True)
        if(len(direction) != 0):
            print("DIRECTIONS => " + direction['data-url'])
        else:
            print("There is no DIRECTIONS")
        # Rating and review count
        # a.Rating
        print("RATING")
        rating_reviews = soup.find_all('div', class_='Ob2kfd')
        #rating_reviews = soup.find_all('div',class_='Ob2asdasdkfd')
        if len(rating_reviews) == 0:
            print("There is no rating_reviews")
        else:
            print("There is rating_reviews")
        ratingSpan = rating_reviews[0].find('span')
        print(ratingSpan.text)
        # b.Review
        reviewHref = rating_reviews[0].find('a', href=True)
        reviewSpan = reviewHref.find_all('span')
        print("REVIEW COUNT")
        print(reviewSpan[0].text)
        # CATEGORY AND PRICE RANGE
        categorySpan = soup.find_all('span', class_='YhemCb')
        if(len(categorySpan) == 1):
            # There will be only Category Field
            print("CATEGORY => ", categorySpan[0].text)
        elif(len(categorySpan) == 2):
            # There will be price range and Category
            print("PRICE RANGE => ", categorySpan[0].text)
            print("CATEGORY => ", categorySpan[1].text)
        elif(len(categorySpan) == 0):
            print("THERE IS NO CATEGORY OR PRICA RANGE")

        # DESCRIPTION
        descriptionParentSpan = soup.find_all('span', class_='ggV7z')
        print("DESCRIPTION")
        print(descriptionParentSpan[0].span.text)
        # ADDRESS AND PHONE
        print('ADDRESS')
        adress_phone = soup.find_all('span', class_='LrzXr')
        print(adress_phone[0].text)
        print('PHONE')
        print(adress_phone[1].span.text)
        # HOURS
        hours = soup.find_all('table', 'WgFkxc')
        days = []
        hourInfo = []
        for hour in hours:
            day = hour.find_all('td')
            print(len(day))
            for i in range(len(day)):
                if i % 2 == 0:
                    days.append(day[i].text)
                else:
                    hourInfo.append(day[i].text)
            print(days)
            print(hourInfo)

        # MENU
        menu = soup.find(text="Menu:").findNext('a')
        if menu is not None:
            menuText = menu.text
            print(menuText)
        else:
            print("No such menu data")
    elif(len(element) > 1):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        three_or_more = soup.find_all('div', class_='zkIadb')
        print("buraya girdi")
        # driver.find_element_by_class_name('zkIadb')
        if len(three_or_more) == 1:
            print("There is more than three element")
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            # F find the button which show link to more businesses
            button_href = soup.find_all('a', class_="cMjHbjVt9AZ__button")
            linkToBusinesses = button_href[0]['href']
            print("Found the URL:", linkToBusinesses)
            url = 'https://www.google.com' + linkToBusinesses
            # url = 'https://www.google.com/search?q=burger%20king%20miami&oq=burger+king+miami+&aqs=chrome..69i57.7221j0j9&sourceid=chrome&ie=UTF-8&npsic=0&rflfq=1&rlha=0&rllag=25778920,-80166606,3044&tbm=lcl&rldimm=1507068975858384699&lqi=ChFidXJnZXIga2luZyBtaWFtaSIDiAEBWiAKC2J1cmdlciBraW5nIhFidXJnZXIga2luZyBtaWFtaQ&ved=2ahUKEwiI5fD7puTnAhVE2-AKHaL-BhUQvS4wAHoECAoQFg&rldoc=1&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m5!1u15!2m2!15m1!1shas_1wheelchair_1accessible_1entrance!4e2!1m5!1u15!2m2!15m1!1shas_1takeout!4e2!2m1!1e3!3sIAE,lf:1,lf_ui:4&rlst=f#rlfi=hd:;si:;mv:[[25.8660221,-80.1292182],[25.731344000000004,-80.32573479999999]]'
            returnOfDriver = driver.get(url)
            element_buttons = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.cXedhc")))
            print(url)
            source_of_page = driver.page_source
            soup = BeautifulSoup(source_of_page, 'html.parser')
            # print(soup.text)
            blas = soup.find_all('div', class_='cXedhc')
            # print(blas)

            element_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.uMdZh")))
            # print(element_buttons)

            if element_buttons:
                # print(element_buttons)
                for el in element_buttons:
                    dataDic = {
                        "name": "",
                        "website": "",
                        "price_range": "",
                        "directions": "",
                        "rating": "",
                        "review_count": "",
                        "category": "",
                        "phone": "",
                        "review_count": "",
                        "description": "",
                        "price_range": "",
                        "address": "",
                        "days": "",
                        "hours": [],
                    }
                    el.click()
                    time.sleep(1)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    divs = soup.find_all('div', class_='xpdopen')
                    # print(len(divs))
                    # BUSINESS NAME
                    header = soup.find_all('div', class_='kno-ecr-pt')
                    if(len(header) != 0):
                        headerText = header[0].find_all('span')
                        print("NAME => " + headerText[0].text)
                        dataDic["name"] = headerText[0].text
                    else:
                        print("There is no name")

                    # WEBSITE
                    website_direction = soup.find_all('div', class_='QqG1Sd')
                    if(len(website_direction) != 0):
                        websiteDiv = website_direction[0].find('a', href=True)
                        print("WEBSITE => " + websiteDiv['href'])
                        dataDic['website'] = websiteDiv['href']
                    else:
                        print("There is no website")

                    # DIRECTIONS
                    direction = website_direction[1].find('a', href=True)
                    if(len(direction) != 0):
                        print("DIRECTIONS => " + direction['data-url'])
                        dataDic['directions'] = direction['data-url']
                    else:
                        print("There is no DIRECTIONS")

                    # Rating and review count
                    # a.Rating
                    print("RATING")
                    rating_reviews = soup.find_all(
                        'div', class_='Ob2kfd')
                    #rating_reviews = soup.find_all('div',class_='Ob2asdasdkfd')
                    if len(rating_reviews) == 0:
                        print("There is no rating_reviews")

                    else:
                        print("There is rating_reviews")
                        ratingSpan = rating_reviews[0].find('span')
                        print(ratingSpan.text)
                        dataDic['rating'] = ratingSpan.text

                    # b.Review
                    reviewHref = rating_reviews[0].find('a', href=True)
                    reviewSpan = reviewHref.find_all('span')
                    print("REVIEW COUNT")
                    print(reviewSpan[0].text)

                    # CATEGORY AND PRICE RANGE
                    categorySpan = soup.find_all(
                        'span', class_='YhemCb')
                    if(len(categorySpan) == 1):
                        # There will be only Category Field
                        print("CATEGORY => ", categorySpan[0].text)
                        dataDic['category'] = categorySpan[0].text
                    elif(len(categorySpan) == 2):
                        # There will be price range and Category
                        print("PRICE RANGE => ", categorySpan[0].text)
                        dataDic['price_range'] = categorySpan[0].text
                        print("CATEGORY => ", categorySpan[1].text)
                        dataDic['category'] = categorySpan[1].text
                    elif(len(categorySpan) == 0):
                        print("THERE IS NO CATEGORY OR PRICA RANGE")
                    # DESCRIPTION
                    descriptionParentSpan = soup.find_all(
                        'span', class_='ggV7z')
                    if len(descriptionParentSpan) != 0:
                        print("DESCRIPTION")
                        print(descriptionParentSpan[0].span.text)
                    # ADDRESS AND PHONE
                    print('ADDRESS')
                    adress_phone = soup.find_all(
                        'span', class_='LrzXr')
                    if len(adress_phone) != 0:
                        print(adress_phone[0].text)
                        #data['address'] = adress_phone[0].text
                        print('PHONE')
                        print(adress_phone[1].span.text)
                        dataDic['phone'] = adress_phone[1].span.text
                    # HOURS
                    hours = soup.find_all('table', 'WgFkxc')
                    if len(hours) != 0:
                        days = []
                        hourInfo = []
                        for hour in hours:
                            day = hour.find_all('td')
                            print(len(day))
                            for i in range(len(day)):
                                if i % 2 == 0:
                                    days.append(day[i].text)
                                else:
                                    hourInfo.append(day[i].text)
                            print(days)
                            dataDic['hours'] = hourInfo
                            print(hourInfo)
                    # MENU
                    menu = soup.find(text="Menu:")
                    if menu is not None:
                        menuText = menu.findNext('a').text
                        print(menuText)
                        dataDic['menu'] = menuText
                    else:
                        print("No such menu data")
                    print(dataDic)
        else:
            print("There is less  and equal to three element")
            map_button = soup.find_all('div', class_='H93uF')
            link_to_businesses = map_button[0].find('a', href=True)
            print(link_to_businesses['href'])
            url = 'https://www.google.com' + \
                link_to_businesses['href'] + "&lr= lang_en"
            driver.get(url)
            element_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.uMdZh")))
            print(len(element_buttons))
            if element_buttons:
                # print(element_buttons)
                for el in element_buttons:

                    dataDic = {
                        "name": "",
                        "website": "",
                        "price_range": "",
                        "directions": "",
                        "rating": "",
                        "review_count": "",
                        "category": "",
                        "phone": "",
                        "review_count": "",
                        "description": "",
                        "price_range": "",
                        "address": "",
                        "days": "",
                        "hours": [],
                    }
                    el.click()
                    time.sleep(1)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    divs = soup.find_all('div', class_='xpdopen')
                    # print(len(divs))
                    # BUSINESS NAME
                    header = soup.find_all('div', class_='kno-ecr-pt')
                    if(len(header) != 0):
                        headerText = header[0].find_all('span')
                        print("NAME => " + headerText[0].text)
                        dataDic["name"] = headerText[0].text
                    else:
                        print("There is no name")
                    # WEBSITE
                    website_direction = soup.find_all(
                        'div', class_='QqG1Sd')
                    print(website_direction)
                    if(len(website_direction) == 1):
                        websiteDiv = website_direction[0].find(
                            'a', href=True)
                        print("WEBSITE => " + websiteDiv['href'])
                        dataDic['website'] = websiteDiv['href']
                    elif len(website_direction) == 2:
                        websiteDiv = website_direction[0].find(
                            'a', href=True)
                        print("WEBSITE => " + websiteDiv['href'])
                        direction = website_direction[1].find(
                            'a', href=True)
                        if(len(direction) != 0):
                            print("DIRECTIONS => " +
                                  direction['data-url'])
                            dataDic['directions'] = direction['data-url']
                        else:
                            print("There is no DIRECTIONS")
                    else:
                        print("There is no website and directions")
                    # Rating and review count
                    # a.Rating
                    print("RATING")
                    rating_reviews = soup.find_all(
                        'div', class_='Ob2kfd')
                    #rating_reviews = soup.find_all('div',class_='Ob2asdasdkfd')
                    if len(rating_reviews) == 0:
                        print("There is no rating_reviews")
                    else:
                        print("There is rating_reviews")
                        ratingSpan = rating_reviews[0].find('span')
                        print(ratingSpan.text)
                        dataDic['rating'] = ratingSpan.text
                        reviewHref = rating_reviews[0].find('a', href=True)
                        if len(reviewHref) != 0:
                            reviewSpan = reviewHref.find_all('span')
                            print("REVIEW COUNT")
                            print(reviewSpan[0].text)
                            match = re.findall(
                                r'^[0-9]+', reviewSpan[0].text)
                            print(match)
                            dataDic['review_count'] = match[0]
                    # b.Review
                    print("te buraya geldi")
                    
                    # CATEGORY AND PRICE RANGE
                    categorySpan = soup.find_all(
                        'span', class_='YhemCb')
                    if(len(categorySpan) == 1):
                        # There will be only Category Field
                        print("CATEGORY => ", categorySpan[0].text)
                        dataDic['category'] = categorySpan[0].text
                    elif(len(categorySpan) == 2):
                        # There will be price range and Category
                        print("PRICE RANGE => ", categorySpan[0].text)
                        dataDic['price_range'] = categorySpan[0].text
                        print("CATEGORY => ", categorySpan[1].text)
                        dataDic['category'] = categorySpan[1].text
                    elif(len(categorySpan) == 0):
                        print("THERE IS NO CATEGORY OR PRICA RANGE")
                    # DESCRIPTION
                    descriptionParentSpan = soup.find_all(
                        'span', class_='ggV7z')
                    if len(descriptionParentSpan) != 0:
                        print("DESCRIPTION")
                        print(descriptionParentSpan[0].span.text)
                    # ADDRESS AND PHONE
                    print('ADDRESS')
                    adress_phone = soup.find_all(
                        'span', class_='LrzXr')
                    if len(adress_phone) != 0:
                        print(adress_phone[0].text)
                        #data['address'] = adress_phone[0].text
                        print('PHONE')
                        print(adress_phone[1].span.text)
                        dataDic['phone'] = adress_phone[1].span.text
                    # HOURS
                    hours = soup.find_all('table', 'WgFkxc')
                    if len(hours) != 0:
                        days = []
                        hourInfo = []
                        for hour in hours:
                            day = hour.find_all('td')
                            print(len(day))
                            for i in range(len(day)):
                                if i % 2 == 0:
                                    days.append(day[i].text)
                                else:
                                    hourInfo.append(day[i].text)
                            print(days)
                            dataDic['hours'] = hourInfo
                            print(hourInfo)
                    # MENU
                    menu = soup.find(text="Menu:")
                    if menu is not None:
                        menuText = menu.findNext('a').text
                        print(menuText)
                        dataDic['menu'] = menuText
                    else:
                        print("No such menu data")
                    print(dataDic)

except:
    print('No data')
finally:
    # driver.quit()
    print("allah")
    #input("Press Enter to continue...")
    sys.exit()
