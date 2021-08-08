from pprint import pprint
import requests, random, pandas as pd
from requests_html import HTML
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


def parse(html):
    global place, city, state, maps_url
    html = HTML(html=html)
    data = {}
    data['key word'] = place
    title = html.xpath('//div[@class="section-hero-header-title"]//h1/span/text()', first=True)
    if title : data['Business Name'] = title
    else : data['Business Name'] = place

    data['Category'] = html.xpath('//div[@class="gm2-body-2"]//span[@class="section-rating-term"]//span/text()', first=True)
    
    try:
        addres = html.xpath('//button[@data-item-id="address"]/@aria-label',first=True)    
    except :
        addres = html.xpath('//button[contains(@aria-label,"Address") or contains(@data-item-id,"address")]/@aria-label',first=True)
    if addres :
         data['address'] = addres.replace('Address: ','')
         data['Zip Code'] = data['address'].split(',')[-2].split()[-1]
    else :
        data['address'] = '-'
        data['Zip Code'] = '-'
    data['City'] = city
    data['State'] = state
    
    data['City'] = city
    data['State'] = state
        
    web = html.xpath('//button[contains(@aria-label,"Website:")]/@aria-label', first=True)
    if web : data['Business Url'] = web.replace('Website: ','www.')
    else : data['Business Url'] = '-'
    
    data['Google Maps Url'] = maps_url
    
    try: data['Average Rating'] = html.xpath('//div[@class="gm2-display-2"]/text()',first=True)
    except: data['Average Rating'] = '-'
    if data['Average Rating'] == '' or data['Average Rating'] == None : data['Average Rating'] = '-'
    rev = html.xpath('//button[contains(text(),"review")]/text()',first=True)
    if rev :  data['Reviews'] = rev.replace('reviews','').replace('review','').strip()
    else : data['Reviews'] = '-'
    
    q = html.xpath('//span[contains(text(),"Questions & answers")]',first=True)
    if q :
        data['# Of Questions Listed?'] = "Yes"
        data['# Of Answers Listed?'] = "Yes"
    else:
        data['# Of Questions Listed?'] = "N/A"
        data['# Of Answers Listed?'] = "N/A"
    
    hours1 = html.xpath('//div[@class="section-open-hours-container cX2WmPgCkHi__container-hoverable"]',first=True)
    hours2 = html.xpath('//*[contains(text(),"Open now") or contains(text(),"Closed. Opens")]',first=True)
    hours3 = html.xpath('//img[@aria-label="Hours"]',first=True)
    hours4 = html.xpath('//span[contains(text(),"See more hours")]',first=True)
    hours5 = html.xpath('//*[contains(text(),"Closed today")]',first=True)
    if hours1 or hours2 or hours3 or hours4 or hours5 :
        data['Business Hours Listed?'] = 'Yes'
    else : data['Business Hours Listed?'] = 'N/A'
    
    book = html.xpath('//*[contains(text(),"booker.com")]', first=True)
    if book :
        data['Reservation/Ordering Listed?'] = 'Yes'
    else : data['Reservation/Ordering Listed?'] = 'N/A'

    menu = html.xpath('//button[@data-item-id="menu"]',first=True)
    if menu :
        data['Cost Information Listed?'] = 'Yes'
    else : data['Cost Information Listed?'] = 'N/A'
    
    lgbtq = html.xpath('//div//*[contains(text(),"LGBTQ-friendly")]', first=True)
    
    try :
        browser.find_element_by_xpath('//div[contains(@aria-label,"About")]/button]').click()
        sleep(5)
    except :
        try :
            browser.find_element_by_xpath("//div[contains(@aria-label,'About ')]//button").click()
            sleep(5)
        except : pass
    sleep(5)
    try : html = HTML(html=browser.page_source)
    except : pass
    
    offering = html.xpath('//ul[contains(@aria-label,"Offerings")]//img[contains(@src,"check")]', first=True)
    payment = html.xpath('//ul[contains(@aria-label,"Payments")]//img[contains(@src,"check")]',first=True)
    accessibility = html.xpath('//ul[contains(@aria-label,"Accessibility")]//img[contains(@src,"check")]',first=True)
    amenities = html.xpath('//ul[contains(@aria-label,"Amenities")]//img[contains(@src,"check")]',first=True)
    planning = html.xpath('//ul[contains(@aria-label,"Planning")]//img[contains(@src,"check")]',first=True)
    identfy = html.xpath('//ul[contains(@aria-label,"Identifies as")]//img[contains(@src,"check")]', first=True)
    crowd = html.xpath('//ul[contains(@aria-label,"Crowd")]//img[contains(@src,"check")]', first=True)
    
    if offering or identfy or payment or accessibility or amenities or planning or lgbtq or crowd :
        data['Business information Listed?'] = 'Yes'
    else : data['Business information Listed?'] = 'N/A'

    services = html.xpath('//ul[@aria-label="Service options"]//img[contains(@src,"check")]',first=True)
    if services :  data['Services Options?'] = 'Yes'
    else : data['Services Options?'] = 'N/A'

    healthy = html.xpath('//ul[contains(@aria-label,"Health and safety") or contains(@aria-label,"Health & safety")] //img[contains(@src,"check")]', first=True)
    if healthy : data['Covid Protection?'] = 'Yes'
    else : data['Covid Protection?'] = 'N/A'
    
    results.append(data)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--lang=en-US')

keywords = pd.read_excel('states.xlsx')['Business Name'].tolist()
maps_links = pd.read_excel('states.xlsx')['Google Maps URL'].tolist()
states = pd.read_excel('states.xlsx')['State'].tolist()
keywords = pd.read_excel('states.xlsx')['Business Name'].tolist()
cities = pd.read_excel('states.xlsx')['City'].tolist()
results = []
passed = []

browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
for i in range(len(maps_links)):
    maps_url = maps_links[i]
    if maps_url != '-' or maps_url != '' or maps_url != None :
        place = keywords[i]
        city = cities[i]
        state = states[i]
        try :
            browser.get(maps_url)
            browser.implicitly_wait(20)
            sleep(10)
            try: browser.find_element_by_xpath('//div[@class="ml-searchbox-button-placeholder ml-ellipsis ml-noselect ml-borderbox"]').click()
            except: pass
            sleep(1)
            try : browser.find_element_by_xpath('//button[@class="ml-promotion-action-button ml-promotion-no-button ml-promotion-no-thanks"]').click()
            except: pass
            try:
                html = browser.page_source
                maps_url = browser.current_url
                parse(html)
                sleep(1)
                df = pd.DataFrame(results)
                df.to_excel(f'Google maps Leads.xlsx',index=False)
                print(f'{datetime.now()} row number {i+1} of {len(keywords)} >>successfuly got data, total results : {len(results)}')
            except : pass
        except : pass
browser.quit()
