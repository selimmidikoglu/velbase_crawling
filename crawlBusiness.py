from bs4 import BeautifulSoup
import re
import time
from selenium.common.exceptions import TimeoutException
def crawl_business(driver):
    #print("Entered the function")
    dataDic = {
        "name": "",
        "website": "",
        "phone": "",
        "address": "",
        "price_range": "",
        "rating": "",
        "review_count": "",
        "category": "",
        "description": "",
        "price_range" : "",
        "days": "",
        "hours" : "",
        "menu": "",
        "facebook": "",
        "youtube": "",
        "twitter": "",
        "instagram": "",
        "status": "",
        "directions": ""
        
    }    
    try:
        element1 = driver.find_element_by_class_name('vk_bk').click
    except: 
        pass
    finally:
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', class_='xpdopen')
        #BUSINESS NAME
        header = soup.find_all('div', class_ = 'kno-ecr-pt')
        if len(header) != 0:
            headerText = header[0].find_all('span')
            #print("NAME => " + headerText[0].text)
            dataDic['name'] = headerText[0].text
        #WEBSITE
        website_direction = soup.find_all('div', class_='QqG1Sd')
        if(len(website_direction) == 2):
            websiteDiv = website_direction[0].find('a',href=True)
            if websiteDiv['href'] != '#':
                #print("WEBSITE => " + websiteDiv['href'])
                dataDic['website'] = websiteDiv['href']
            direction = website_direction[1].find('a',href=True)
            if(len(direction) != 0):
                #print("DIRECTIONS => " + direction['data-url'])
                dataDic['directions'] = direction['data-url']
            else:
                x = 5
                #print("There is no DIRECTIONS")
        elif(len(website_direction) == 1):
            websiteDiv = website_direction[0].find('a',href=True)
            if websiteDiv.text == 'Directions' and websiteDiv['data-url'] != '#' :
                 #print("Direction bulundu")
                 #print("DIRECTIONS => " + websiteDiv['data-url'])
                 dataDic['directions'] = websiteDiv['data-url']
            elif websiteDiv.text == 'Website':
                 #print("Direction bulundu")
                 #print("WEBSITE => " + websiteDiv['href'])
                 dataDic['website'] = websiteDiv['href']
                 
        else:
            x = 5
            #print("There is no direction or website")
             
        #STATUS
        '''status = soup.find_all('span',class_="TLou0b")
        if len(status) == 0:
                x = 5
        
        else:
            status = status[0].span.b.text
            dataDic['status'] = status'''
        #DIRECTIONS
        
        #Rating and review count
        #a.Rating
        
        rating_reviews = soup.find_all('div',class_='Ob2kfd')
        #rating_reviews = soup.find_all('div',class_='Ob2asdasdkfd')
        if len(rating_reviews) == 0:
            x = 5
            #print("There is no rating_reviews")
        else:
            #print("There is rating_reviews")
            #print("RATING")
            ratingSpan = rating_reviews[0].find('span')
            #print(ratingSpan.text)
            dataDic['rating'] = ratingSpan.text
            #b.Review
            reviewHref = rating_reviews[0].find('a',href=True)
            if len(reviewHref) != 0:
                reviewSpan = reviewHref.find_all('span')
                #print("REVIEW COUNT")
                #print(reviewSpan[0].text)
                dataDic['review_count'] = str(int(re.search(r'\d+', reviewSpan[0].text).group()))
                
        

        
        #CATEGORY AND PRICE RANGE
        categorySpan = soup.find_all('span',class_='YhemCb')
        if(len(categorySpan) == 1):
            #There will be only Category Field
            #print("CATEGORY => ", categorySpan[0].text)
            dataDic['category'] = categorySpan[0].text
        elif(len(categorySpan) == 2):
            #There will be price range and Category
            #print("PRICE RANGE => ", categorySpan[0].text)
            dataDic['price_range'] = categorySpan[0].text
            #print("CATEGORY => ", categorySpan[1].text)
            dataDic['category'] = categorySpan[1].text
        elif(len(categorySpan) == 0):
            x = 5
            #print("THERE IS NO CATEGORY OR PRICA RANGE")
        
        
        #DESCRIPTION
        descriptionParentSpan = soup.find_all('span',class_='ggV7z')
        
        if len(descriptionParentSpan) != 0:
            #print("DESCRIPTION => ",descriptionParentSpan[0].span.text)
            dataDic['description'] = descriptionParentSpan[0].span.text
        #ADDRESS AND PHONE
        #address_phone_span_count = soup.find_all('span',class_="w8qArf")
        adress_phone = soup.find_all('span',class_='LrzXr')
        adress_or_phone = soup.find_all('span',class_ = 'w8qArf')
        if len(adress_phone) == 2:
            #print('ADDRESS')
            #print(adress_phone[0].text)
            dataDic['address'] = adress_phone[0].text
            #print('PHONE')
            #print(adress_phone[1].span.text)
            dataDic['phone'] = adress_phone[1].span.text
        elif len(adress_phone) == 1:
            if adress_phone[0].text != '':
                #print('PHONE')
                #print(adress_phone[0].text)
                if(adress_or_phone[0].a.text.startswith('A')):
                    dataDic['address'] = adress_phone[0].text
                else:
                    dataDic['phone'] = adress_phone[0].text



        #HOURS
        hours = soup.find_all('table','WgFkxc')
        days = []
        hourInfo = []
        for hour in hours:
            day = hour.find_all('td')
            ##print(len(day))
            for i in range(len(day)):
                if i % 2 == 0:
                    days.append(day[i].text)
                else:
                    hourInfo.append(day[i].text)
            #print(days)
            #print(hourInfo)
            strHours = ""
            for hour in hourInfo:
                strHours += hour+ " "
            dataDic['hours'] = strHours
        
        #MENU
        menu = soup.find(text="Menu:")
        if menu is not None:
            menuText = menu.findNext('a').text
            #print(menuText)
            dataDic['menu'] = menuText
        else:
            x = 5
            #print("No such menu data")

        profiles = soup.find_all('div',class_="PZPZlf kno-vrt-t")
        if len(profiles) != 0:
            for profile in profiles:
                text = profile.a['href']
                if re.findall('facebook',text):
                    #print("FACEBOOK => ", text)
                    dataDic['facebook'] = text
                elif re.findall('twitter',text):
                    #print("TWITTER =>",text)
                    dataDic['twitter'] = text
                elif re.findall('youtube',text):
                    #print("YOUTUBE =>",text)
                    dataDic['youtube'] = text
                elif re.findall('instagram',text):
                    #print("INSTAGRAM =>",text)
                    dataDic['instagram'] = text
        print(dataDic)
        return dataDic