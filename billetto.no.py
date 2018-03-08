#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 23:07:07 2018

@author: dipu
"""


import os
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from dateutil.parser import parse
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import csv
import re
from pathlib import Path
from collections import OrderedDict
import urllib.request
import datetime
from dateutil import parser
fields = OrderedDict([('ai_id', ''),
('category', ''),
('event_name', ''),
('event_desc', ''),
('start_date', ''),
('start_time', ''),
('end_date', ''),
('end_time', ''),
('host_name', ''),
('location_name', ''),
('location_address', ''),
('location_desc', ''),
('host_contact', ''),
('lat', ''),
('lng', ''),
('image_name', ''),
('city', ''),
('ticket_link', ''),
('facebookhost_id', ''),
('website', ''),
('facebook_id', ''),
('linkedin_id', ''),
('twitter_id', ''),
('instagram_id', ''),
('pinterest_id', ''),
('google_id', ''),
('skype_id', ''),
('youtube_id', ''),
('discord_id', ''),
('snapchat_id', ''),
('ello_id', ''),
('periscope_id', ''),
('vimeo_id', ''),
('meerkat_id', ''),
('vine_id', ''),
('flickr_id', ''),
('tumblr_id', ''),
('medium_id', ''),
('tripadvisor_id', ''),
('dribble_id', ''),
('whatsapp_id', ''),
('search_value',''),
('parent_event',''),
('marker',''),
('site_scraped','')])

def get_month(month):
    month=str(month)
    month=month[:3]
    month=str.lower(month)
    print("Month:"+month)
    if month == "jan": return '01'
    elif month== "feb": return '02'
    elif month== "mar": return '03'
    elif month== "apr": return '04'
    elif month== "mai": return '05'
    elif month== "jun": return '06'
    elif month== "jul": return '07'
    elif month== "aug": return '08'
    elif month== "sep": return '09'
    elif month== "okt": return '10'
    elif month== "nov": return '11'
    elif month== "des": return '12'
    else: return ''

def convert_to_date(day,month,year,time):
    month=get_month(month)
    
    date=year+'-'+month+'-'+day+'T'+time
    print("DAte:"+date)
    try:
        dt=parser.parse(year+'-'+month+'-'+day+'T'+time)
        return dt
    except:
        return None


dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--ignore-certificate-errors')
#chromeOptions.add_argument('--headless')

chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(dir_path+'/chromedriver',chrome_options=chromeOptions)
#driver = webdriver.Chrome(dir_path+'/chromedriver')
#driver.implicitly_wait(1)

container_path=dir_path+'/containers.csv'
host_map={}
map_lat=dict()
map_lng=dict()
map_addr=dict()
header = list(fields.keys())
page=0
folder=dir_path+'/billetto.no'
csvfile = folder+'/billetto.no.csv'
try:
    if not os.path.exists(folder):
        os.makedirs(folder)
except:
    print("Folder Exist")
with open(csvfile, "w", encoding='utf-8') as output:
    writer = csv.writer(output, lineterminator='\n')
    if(page==0):
        writer.writerow(header)
count=0
for page in range(1,5,1):
    
    img_folder = folder + '/images'
    
    
    try:
        print(folder)
        os.mkdir(folder)
    except:
        print("Folder Exist")
    page_id=1
    next_page = 'https://billetto.no/no?text=&page='+str(page)+'&is_v=1'
    print(next_page)
    print("================================")
    driver.get(next_page)
    sleep(2)
    #click for norway language
    main_window = driver.current_window_handle
    rows=driver.find_elements_by_css_selector('#hits_container > div > div')
    event_count=1
    count=0
    for row in rows:
        count+=1;
        if(count<5):
            continue;
        print("Count:"+str(count))
        count+=1
        event_link=row.find_element_by_css_selector('div > div > a').get_attribute('href')
        event_link=event_link.replace('https://billetto.no/en/','https://billetto.no/no/')
        fields['site_scraped']=event_link
        print('Event Link:'+event_link)
        #get category
        category=row.find_element_by_css_selector("div > div > div > div > div > div.span10 > p > a").text
        fields['category']=category
        #get host name
        try:
            host_name=driver.find_element_by_css_selector('#hits_container > div > div:nth-child(3) > div > div > a > div.event-card__content > p').text
            print("Host:"+host_name)
            fields['host_name']=host_name
        except:
            print("host name not found")
        
        
        #open new tab 
        try:
            print("GEt Event Link:"+event_link)
            driver.execute_script("window.open('');")            
            #event_link_ele.send_keys(Keys.CONTROL+Keys.RETURN)
            driver.switch_to_window(driver.window_handles[1])
            
            driver.get(event_link)
            
        except:
            print(traceback.format_exc())
            print("Event link not clickable")
        
        
        #get date
        try:
            try:
                time_info=driver.find_element_by_css_selector('#js-content > div.shame-remove-header-margin.single-event > div.app-card-light > div > div > div > div > div.grid__item.five-eighths > div > div:nth-child(1) > div > div:nth-child(1) > p').text
            except:
                print("Time not found")
            
            try:
                start_time_info=time_info.split("-")[0]
            except:
                print("Start time not found")
            try:
                end_time_info=time_info.split("-")[1]
            except:
                print("End time not found")
            
            date_split=start_time_info.split()
            try:
                start_day=date_split[0][:-1]
            except:
                print("Start day not found")
            try:
                start_month=date_split[1]
            except:
                print("Start month not found")
            
            try:
                start_year=date_split[2][:-1]
            except:
                print("Start year not found")
            try:
                start_time=date_split[3]
            except:
                print("Start time not found")
            
            dt=convert_to_date(start_day,start_month,start_year,start_time)
            start_date=dt.strftime('%d-%m-%Y')
            fields['start_date']=start_date
            fields['start_time']=dt.strftime("%H:%M")
            print(dt)
            date_split=end_time_info.split()
            try:
                end_day=date_split[0][:-1]
            except: 
                print("End day not found")
            try:
                end_month=date_split[1]
            except:
                print("end month not found")
            
            try:
                end_year=date_split[2][:-1]
            except:
                print("End year not found")
            try:
                end_time=date_split[3]
            except:
                print("End time not found")
            
            dt=convert_to_date(end_day,end_month,end_year,end_time)
            end_date=dt.strftime('%d-%m-%Y')
            fields['end_date']=end_date
            fields['end_time']=dt.strftime("%H:%M")
            
            print(dt)
        except:
            print("DAte not Found")
        #get event name
        try:
            event_name=driver.find_element_by_css_selector('#js-content > div.shame-remove-header-margin.single-event > div.single-event-header > div.grid-container > div > h1').text
            print("event Name:"+event_name)
            fields['event_name']=event_name
        except:
            print("Event name not found")
        
        
        #get organizer
                
        try:
            organizer=driver.find_element_by_css_selector('#js-content > div.shame-remove-header-margin.single-event > div.app-card-light > div > div > div > div > div.grid__item.five-eighths > div > div:nth-child(2) > div > div.grid__item.nine-tenths > a:nth-child(1) > p > font > font').text
            print("Organizer:"+organizer)
            fields['organizer']=event_name
        except:
            print("Organizer not found")
        
        #get organizer contact
        try:
            organizer_page=driver.find_element_by_css_selector("#js-content > div.shame-remove-header-margin.single-event > div.app-card-light > div > div > div > div > div.grid__item.five-eighths > div > div:nth-child(2) > div > div.grid__item.nine-tenths > a:nth-child(1)")
            
        except:
            print("Organizer not found")
        #get organizer contact
        try:
            organizer_contact=driver.find_element_by_css_selector("#js-content > div.shame-remove-header-margin.single-event > div.app-card-light > div > div > div > div > div.grid__item.five-eighths > div > div:nth-child(2) > div > div.grid__item.nine-tenths > a.typography--milli.push--right")
            
        except:
            print("Organizer not found")
         
            
        #get city
        try:
            city=driver.find_element_by_css_selector('a > div.artistticket__detailscontainer > section > h5').text
            print("City:"+city)
            fields['city']=city
        except:
            print("city name not found")
        
        
        
        
        #get event details
        try:
            event_desc=driver.find_element_by_css_selector('#js-content > div.shame-remove-header-margin.single-event > div.grid-container > div > div > div > div.grid__item.five-eighths > div').text
            print("Event Detail:"+event_desc)
            fields['event_desc']=event_desc
            
        except:
            print(traceback.format_exc())
            print("event_desc  not found")
        
        #get ticket link
        try:
            ticket_link=driver.find_element_by_css_selector('#js-content > div.shame-remove-header-margin.single-event > div.app-card-light > div > div > div > div > div.grid__item.three-eighths > div > div > div.js-scroll-follow.single-event-aside.chamber-half.text--center > div.single-event-aside__ticket-button-container > a').get_attribute("href")
            print("Ticket link:"+ticket_link)
            fields['ticket_link']=ticket_link
        except:
            print(traceback.format_exc())
            print("ticket link not found")
        
        try:                
            image_link=driver.find_element_by_css_selector('#js-content > div.shame-remove-header-margin.single-event > div.single-event-header').get_attribute('style')
            image_link=image_link[image_link.find('(')+1:image_link.rfind(')')]
            print("Image Link:"+image_link)
        except:
            
            print("No Image link")
        #download image
        try:
            print("Image link:"+image_link)
            img_src=''
            if(str.find(image_link,"http")>=0 or str.find(image_link,"www")>=0):
                img_src=image_link[:image_link.rfind("?")]
            else:
                if(len(image_link)>0):
                    img_src = "http://"+image_link[:image_link.rfind("?")]
            
            print("image src:"+img_src)
            x = img_src.split('/')[-1]
            #print("Image Name:"+x);
            fields['image_name']=x
            save_path = folder+"/"+x
            #print("Save_path:"+save_path)
            if(len(img_src)>0):
                urllib.request.urlretrieve(img_src, save_path)
        except Exception:
            print('no image')
            print(traceback.format_exc())
        '''
        try:
                calendar=driver.find_element_by_css_selector("#entity_44014 > div > aside > div:nth-child(2) > div.text-center > a").get_attribute("href")
                calendar=driver.current_url+calendar
                google_id=driver.find_element_by_css_selector("#root > table > tbody > tr > td > a").get_attribute("href") 
                twitter_id=driver.find_element_by_css_selector("#b").get_attribute("href")
        except:
                print("Social links not found")
        '''
        
        #get location name
        try:
            location_name=driver.find_element_by_css_selector('#js-content > div.shame-remove-header-margin.single-event > div.app-card-light > div > div > div > div > div.grid__item.five-eighths > div > div:nth-child(1) > div > div:nth-child(2) > p').text
            
            print("Location Name:"+location_name)
            fields['location_name']=location_name
        except:
            print(traceback.format_exc())
            print("location_name name not found")
        #location address
        try:
            location_address=driver.find_element_by_css_selector('#top > main > div > div.layout__container > div.accordion__accordion > div > div > h3').text
            location_address=location_name.split(",")[0]+","+location_address
            print("Location address:"+location_address)
            fields['location_address']=location_address
        except:                
            print("Location Detail not found")
        
        #get latitute longitute and location
        #lat_lng
            
        try:
            if(fields['location_name'] not in map_lat or fields['location_name'] not in map_lng ):
                driver.get('https://www.latlong.net/')
                inputEle = driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > input')
                inputEle.send_keys(fields['location_address']+", Norway")
                driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > button').click()
                #latitude
                lat=''
                
                #longitude
                lng=''
                
                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                                   'Timed out waiting for PA creation ' +
                                                   'confirmation popup to appear.')
                    alert = driver.switch_to.alert
                    alert.accept()
                    print("alert accepted")
                except TimeoutException:
                    print("no alert")
                    lat=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div > input').get_attribute('value')
                    lng=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div:nth-child(2) > input').get_attribute('value')
                    fields['lat'] = str(lat)
                    fields['lng'] = str(lng)
                    print(fields['lat'])
                    print(fields['lng'])
                    map_lat[fields['location_name']]=lat
                    map_lng[fields['location_name']]=lng
                    print("Pass 3")
                    sleep(5)
                    pass
            else:
                  fields['lat'] = map_lat[fields['location_name']]
                  fields['lng'] = map_lng[fields['location_name']]
                  
            
        except:
            print("error in  latlong.net")
            print(traceback.format_exc())
        
        
        
        
        
        
        #fill details
        print("-------------Start----------------------")
        with open(csvfile, "a", encoding='utf-8') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(list(fields.values()))
            print("===================================================");
            print("===================================================");
            
            print("Count:"+str(event_count)+" Image:"+fields['image_name'])
            print("Start Time:"+start_time)
            print("Event:"+fields['event_name'])
            print("Image:"+fields['image_name'])
            print("location Name:"+fields['location_name'])
            print("Location Address:"+fields['location_address'])
            print("Ticket Link:"+fields['ticket_link'])
            print("site_scraped:"+fields['site_scraped'])
            print("Host NAme:"+fields['host_name'])
            print("Event Desc:"+fields['event_desc'])
            
            print("Lat :"+fields['lat'])
            print("Lng:"+fields['lng'])
            print("===================================================");
            print("===================================================");
            
            
            event_count+=1
            #print(list(fields.values()))
            #print(fields)
            fields = fields.fromkeys(fields, '')
            sleep(1)
            if(len(driver.window_handles)>1):
                driver.switch_to_window(driver.window_handles[1])
                driver.close()
            driver.switch_to_window(driver.window_handles[0])
            
            #driver.switch_to_window(main_window)
            #sleep(5)
            
            print("----------------End-------------------")
            
    
