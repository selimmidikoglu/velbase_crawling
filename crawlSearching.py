from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
import sys
import time
from selenium.webdriver.support import expected_conditions as EC
#from configDataBase import connectToDB
from selenium.common.exceptions import TimeoutException
#from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from urllib3.exceptions import ProtocolError
from crawlBusiness import crawl_business
import os
from threading import Thread
mainUrl = "http://www.google.com/search?q="

os.environ['MOZ_HEADLESS_WIDTH'] = '1920'
os.environ['MOZ_HEADLESS_HEIGHT'] = '1080'


options = Options()
#options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
#options.add_argument("--window-size=1920x1080") #I added this
options.add_argument("--ignore-certificates-errors")
options.add_argument("--width=1920")
options.add_argument("--height=1080")
webdriver.DesiredCapabilities.FIREFOX['marionette'] = True
'''webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
    "httpProxy":"http://intenwin:42e7c5-889eb2-964986-465bf4-9acc5e@megaproxy.rotating.proxyrack.net:222",
    #"ftpProxy":"intenwin:42e7c5-889eb2-964986-465bf4-9acc5e@megaproxy.rotating.proxyrack.net:222",
    #"sslProxy":"intenwin:42e7c5-889eb2-964986-465bf4-9acc5e@megaproxy.rotating.proxyrack.net:222",
    "proxyType":"MANUAL",
    #"class":"org.openqa.selenium.Proxy",
    #"autodetect":False
}'''

profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", "megaproxy.rotating.proxyrack.net")
profile.set_preference("network.proxy.http_port", "222")
profile.set_preference("network.proxy.socks_username", "intenwin")
profile.set_preference("network.proxy.socks_password", "42e7c5-889eb2-964986-465bf4-9acc5e")
profile.update_preferences()
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
                "price_range" : "",
                "address": "",
                "days": "",
                "hours" : [],
            }
def emptyDataDic():
    dataDic = {"name": "","website": "","price_range": "","directions": "","rating": "","review_count": "","category": "","phone": "","review_count": "","description": "","price_range" : "","address": "","days": "","hours" : []}
    return dataDic
def openABrowserAndSearch(i,data):
    print("Thread " +  str(i) + " STARTED")
    #print(data)
    driver = webdriver.Firefox(firefox_options= options, firefox_profile=profile)
    #for row in data:
    driver.get(mainUrl + data[0].replace(" ", "+") + "+" + data[1].replace(" ","+") + "+" + data[2] + "&lr=lang_en")
    try:
        element = WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cXedhc,div.fYOrjf")))
        if(len(element) == 1):
            dataDic = emptyDataDic()
            element1 = driver.find_element_by_class_name('vk_bk').click
            print("Girdi")
            crawl_business(driver)
        elif(len(element) > 1):
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            three_or_more = soup.find_all('div',class_ = 'zkIadb')
            if len(three_or_more) == 1:
                print("There is more than three element")
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                #F find the button which show link to more businesses
                button_href = soup.find_all('a', class_="cMjHbjVt9AZ__button")
                linkToBusinesses = button_href[0]['href']
                print("Found the URL:", linkToBusinesses )
                url = 'https://www.google.com' + linkToBusinesses
                print(url)
                driver.get(url)
                element_buttons = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.cXedhc")))
                if element_buttons:
                    for el in element_buttons:
                        el.click()
                        time.sleep(1)
                        crawl_business(driver)
        else:
            print("There is less  and equal to three element")
            map_button = soup.find_all('div', class_='H93uF')
            link_to_businesses = map_button[0].find('a', href=True)
            
            url = 'https://www.google.com' + link_to_businesses['href'] 
            print(url)
            driver.get(url)
            print(driver.page_source)
            element_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.uMdZh")))
            print(len(element_buttons))
            if element_buttons:
                #print(element_buttons)
                for el in element_buttons:
                    el.click()
                    time.sleep(1)
                    element_buttons = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.xpdopen")))
                    crawl_business(driver)
    except:
        print("Birşeyler oldu")
    finally:
        x = input("Enter")
        if x == "Q":
            driver.close()
            sys.exit()
        driver.close()
    print("Thread " +  str(i) + " FINISHED")
    

if __name__ == '__main__':
    threads = []
    rows = (('DYED, FRIED AND COMBED TO THE SIDE, INC.', 'WEST HOLLYWOOD', 'CA'), ('Sands Accounting Services', 'LIBERTY', 'IN'), ('Goff Seafood', 'ALEXANDRIA', 'LA'), ('Crown Tenant Advisors, Inc.', 'ROSWELL', 'GA'), ('FROST CORPORATE SERVICES, INC.', 'POMPANO BEACH', 'FL'), ('Harriet S Stitchery', 'ABILENE', 'KS'), ('YEPEZ AJUSTIN', 'CHICAGO', 'IL'), ('LEAPMATRIX', 'ALGONQUIN', 'IL'), ('GOLDNER PAPANDON CHILDS & DELUCCIA LLC', 'MEDIA', 'PA'), ('GEBILSEA LEASING INC', 'FAIR GROVE', 'MO'), ('BUCHANAN ENTERPRISES INC', 'MIDDLETOWN', 'MD'), ('KRISTINE L HAWES-AIKEN', 'ESCANABA', 'MI'), ('ALL TRIM', 'APPLETON', 'WI'), ("FONDATION POUR L'ENFANCE OF AMERICA, INC.", 'NORTH PALM BEACH', 'FL'), ('HAL BOYD', 'RICHARDSON', 'TX'), ('Sensation', 'SAN DIEGO', 'CA'), ('Campbell Inc., Melanie', 'WOODBRIDGE', 'VA'), ("Mike's Jewelry", 'PASSAIC', 'NJ'), ('Brian Lewis & Company, Certified Public Accountants, A Professional Corporation', 'LOS ANGELES', 'CA'), ('Angelica Rowlands', 'LYNCHBURG', 'OH'), ('FUTURE LYFE PUBLISHING', 'KATY', 'TX'), ('DAISY E PICCIRELLI ENTERPRISES', 'MESA', 'AZ'), ('Blessed By The Best, LLC', 'SAINT CLOUD', 'MN'), ('AMERICANA SYSTEMS INC', 'TROY', 'MI'), ('RR Natural Health Inc', 'STREAMWOOD', 'IL'), ('J E Wheeler Quail Farm', 'MINTER', 'AL'), ('LINK COLLATERAL', 'LEXINGTON', 'SC'), ('WEBSTER SCALE', 'OAKES', 'ND'), ('ALICE MARIE ROBERTS', 'DE KALB', 'TX'), ('Hardesty Enterprises Ltd', 'PEORIA', 'IL'), ('James W Easley', 'COLUMBUS', 'OH'), ('EIC MARKETING CORPORATION', 'MURRAY', 'UT'), ('RALPH H CROOK', 'HARTSVILLE', 'TN'), ("RODRIGUEZ'S FURNITURE", 'DALLAS', 'TX'), ('TEC Stormcube', 'MILFORD', 'CT'), ('ROSA A MANTILLA', 'WAYNE', 'NJ'), ('HICKORYDOCC.ORG', 'HICKORY', 'NC'), ('Rcms Group LLC', 'ALPHARETTA', 'GA'), ('DANIEL C GREEN', 'COUNCIL', 'ID'), ('David E Hathaway Atty', 'ADA', 'MI'), ('REELE CORP.', 'TORRANCE', 'CA'), ('Zeal', 'RANDALLSTOWN', 'MD'), ('BENJAMIN S JORY', 'TURTLETOWN', 'TN'), ('FLOOR CHANGERS', 'RODEO', 'CA'), ('ROSEWELL, LLC', 'SOUTHPORT', 'CT'), ('VENTURE SIX MANAGEMENT, L.L.C.', 'KANSAS CITY', 'MO'), ('SHOW PONY, LLC', 'BEDFORD', 'NH'), ('Bennetttrent', 'BOISE', 'ID'), ('CHAUDHARY, ZAIN UL', 'LONG ISLAND CITY', 'NY'), ('Lhct-Dks Partners, L.P.', 'DALLAS', 'TX'), ('S Med Inc', 'SHELTON', 'WA'), ('DCR IMAGES', 'HOWELL', 'MI'), ('Lumsden Farms, Inc.', 'DE WITT', 'AR'), ('JACOB PETLICK', 'BENTON HARBOR', 'MI'), ('THE J T A M FUND LLC', 'PARADISE VALLEY', 'AZ'), ('Red Wing Transport, Inc.', 'COLUMBIA', 'PA'), ('Odyssey A Community of Integral Learning, Inc.', 'ASHEVILLE', 'NC'), ('JOHN M GREENE INC', 'HIGH POINT', 'NC'), ('GET RESULTS, INC.', 'INDIANAPOLIS', 'IN'), ('JAMIE L HUTCHINS', 'NEW HAMPTON', 'NH'), ('GLSA FINANCIAL & INSURANCE', 'ORANGE', 'CA'), ('Hi-Point Signs LLC', 'BELLEVIEW', 'FL'), ('Breakthrough Education Strategies, LLC', 'WEST HARTFORD', 'CT'), ('TENACIOUS TEENS 4 CHRIST', 'FAIRVIEW', 'TN'), ('TRANS VAIL INC', 'MEEKER', 'CO'), ('Bruce Mennella', 'BURIEN', 'WA'), ('AMPARAN SONS TRUCKING', 'WALNUT', 'CA'), ('GRUMPY CUSTOMS INC.', 'MIAMI', 'FL'), ('Allen Wain MD', 'KAMAS', 'UT'), ('Razorline Media & Services LLC', 'INDIANAPOLIS', 'IN'), ('SALAS AUTO AND TOWING SERVICE', 'CEDAR HILL', 'TX'), ('HEAVENLY HAIR LLC', 'WEST COLUMBIA', 'SC'), ('JENNINGS PACIFIC, LLC', 'KOLOA', 'HI'), ('Brown & Kennedy LLC', 'NASHVILLE', 'TN'), ('Options Treatment Programs Inc', 'OSHKOSH', 'WI'), ('SRRC PROPERTIES L.L.C.', 'SCOTTSDALE', 'AZ'), ('Supreme Court, United States', 'INDIANAPOLIS', 'IN'), ('The Rooter Service', 'SAN JOSE', 'CA'), ('Melissa Ludwig', 'MINNEAPOLIS', 'MN'), ('INDEPENTDENT BEAUTY CONSULTANT', 'TEMPLE', 'TX'), ('Matthews Painting and Drywall', 'BOGALUSA', 'LA'), ('The Printer Marge', 'LOMBARD', 'IL'), ("Del's Television Inc", 'WATERBURY', 'CT'), ('BMT CITY PROJECT MGR', 'VIDOR', 'TX'), ('Bryan Schoneboom', 'SACHSE', 'TX'), ("O'Reilly Automotive, Inc.", 'HIRAM', 'GA'), ("La Brue's Cabinets", 'YUBA CITY', 'CA'), ('Rick Gatlin Wholesale Car', 'FORT WORTH', 'TX'), ('Auburn University', 'HUNTSVILLE', 'AL'), ('MCBURNETT & JERNIGAN CONSTRUCTION INC', 'PUNTA GORDA', 'FL'), ('Fred L Wishenhunt', 'CITRUS HEIGHTS', 'CA'), ('BILLY J BANCROFT', 'HEARNE', 'TX'), ('US CENSUS BUREAU', 'MERIDIAN', 'MS'), ('Bella Vita Property Management, Inc.', 'MELBOURNE', 'FL'), ('E02 CONCEPTS', 'SAN ANTONIO', 'TX'), ('CHAVEZ, CLAUIDO', 'DELTA', 'CO'), ('RB Tile, LLC', 'BOISE', 'ID'), ('STORYCHARTS LLC', 'PASADENA', 'CA'), ('HILLIAN MILLWORK', 'NORMAN', 'OK'), ('DEB SANDY S DELIGHT', 'WINDSOR MILL', 'MD'))
    print("MYSQL DATA RETRIEVED")
    for i in range(20):
        threads.append(Thread(target = openABrowserAndSearch, args=(i, rows[i])))
        #threads.append(Thread(target = openABrowserAndSearch, args=(i, rows[(i*10):(i+1)*10])))
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

        
        
        
            