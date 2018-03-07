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
chromeOptions.add_argument('--headless')

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
folder=dir_path+'/livenation.no'
csvfile = folder+'/livenation.no.csv'
try:
    if not os.path.exists(folder):
        os.makedirs(folder)
except:
    print("Folder Exist")
with open(csvfile, "w", encoding='utf-8') as output:
    writer = csv.writer(output, lineterminator='\n')
    if(page==0):
        writer.writerow(header)
    
for page in range(1,6,1):
    
    img_folder = folder + '/images'
    
    
    try:
        print(folder)
        os.mkdir(folder)
    except:
        print("Folder Exist")
    page_id=1
    next_page = 'https://www.livenation.no/event/allevents?page='+str(page)
    print(next_page)
    print("================================")
    driver.get(next_page)
    sleep(2)
    #click for norway language
    main_window = driver.current_window_handle
    rows=driver.find_elements_by_css_selector('#top > main > div > div.layout__container > ul > li')
    event_count=1
    count=0
    for row in rows:
        sleep(3)     
        print("Count:"+str(count))
        count+=1
        event_link=row.find_element_by_css_selector('a').get_attribute('href')
        #event_link='https://www.livenation.no/'+event_link
        fields['site_scraped']=event_link
        print('Event Link:'+event_link)
        event_link_ele=row.find_element_by_css_selector('a')
        #get date
        try:
            try:
                day=row.find_element_by_css_selector('a > div.artistticket__date > span.date__day').text
            except:
                print("day not found")
            try:
                month,year=row.find_element_by_css_selector('a > div.artistticket__date > span.date__month').text.split()
            except:
                print("month year  not found")
            
            
            dt=convert_to_date(day,month,year,'00:01')
            start_date=dt.strftime('%d-%m-%Y')
            fields['start_date']=start_date
            print("Date:"+start_date)
            fields['end_date']=start_date
        except:
            print("DAte not Found")
        #get event name
        try:
            event_name=row.find_element_by_css_selector('a > div.artistticket__detailscontainer > section > h3 > span').text
            print("event Name:"+event_name)
            fields['event_name']=event_name
        except:
            print("Event name not found")
        
        #get host name
        try:
            host_name=driver.find_element_by_css_selector('a > div.artistticket__detailscontainer > section > h4.artistticket__venue').text
            print("Host:"+host_name)
            fields['host_name']=host_name
        except:
            print("host name not found")
        
        #get city
        try:
            city=driver.find_element_by_css_selector('a > div.artistticket__detailscontainer > section > h5').text
            print("City:"+city)
            fields['city']=city
        except:
            print("city name not found")
        
        try:
            print("GEt Event Link:"+event_link)
            driver.execute_script("window.open('');")            
            #event_link_ele.send_keys(Keys.CONTROL+Keys.RETURN)
            driver.switch_to_window(driver.window_handles[1])
            
            driver.get(event_link)
            
        except:
            print(traceback.format_exc())
            print("Event link not clickable")
        
        
        
        #get event details
        try:
            event_desc=driver.find_element_by_css_selector('#top > main > div > div.layout__container > div.accordion__accordion > div').text
            print("Event Detail:"+event_desc)
            fields['event_desc']=event_desc
            
            #get start time from desc
            pattern="(?i)(Dører)(\W+)(\W+)([0-9]{0,2}:[0-9]{0,2})"
            match=re.search(pattern,event_desc)
            print("match result:")
            print(match)
            match_start=''
            if(match!=None):
                match_start=match[0].split()[1]
                print("Start Time from Event---->: desc: "+match[0])
        except:
            print(traceback.format_exc())
            print("event_desc  not found")
        
        
        try:                
            image_link=driver.find_element_by_css_selector('#top > main > div > div.layout__container > div.eventblurb > section').get_attribute('style')
            image_link=image_link[image_link.find('"')+3:image_link.rfind('"')]
            print("Image Link:"+image_link)
        except:
            
            print("No Image link")
        #download image
        try:
            print("Image link:"+image_link)
            img_src=''
            if(str.find(image_link,"http")>=0 or str.find(image_link,"www")>=0):
                img_src=image_link
            else:
                if(len(image_link)>0):
                    img_src = "http://"+image_link
            
            #print("image src:"+img_src)
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

        
        
        #get location name
        try:
            location_name=driver.find_element_by_css_selector('#top > main > div > div.layout__container > div.eventblurb > div > div.eventblurb__detailscontainer > h2').text
            location_name=location_name.replace("Detaljer","")
            print("Location Name:"+location_name)
            fields['location_name']=location_name
        except:
            print(traceback.format_exc())
            print("location_name name not found")
        #top > main > div > div.layout__container > div.eventblurb > section
        
        #get ticket link
        try:
            ticket_link=driver.find_element_by_css_selector('#top > main > div > div.layout__sidebar > section > div > a').get_attribute("href")
            print("Ticket link:"+ticket_link)
            fields['ticket_link']=ticket_link
        except:
            print(traceback.format_exc())
            print("ticket link not found")
        
        
        
        #get location link
        try:
            location_link=driver.find_element_by_css_selector('#top > main > div > div.layout__container > div.eventblurb > div > div.eventblurb__detailscontainer > h2 > a').get_attribute("href")
            #go to link
            #location_link.send_keys(Keys.CONTROL+Keys.RETURN)
            print("GEt location link:"+location_link)
            driver.get(location_link)
            driver.switch_to_window(driver.window_handles[1])
            #location address
            try:
                location_address=driver.find_element_by_css_selector('#top > main > div > div.layout__container > div.accordion__accordion > div > div > h3').text
                location_address=location_name.split(",")[0]+","+location_address
                print("Location address:"+location_address)
                fields['location_address']=location_address
            except:                
                print("Location Detail not found")
            
            
            
            #get location detail
            try:
                location_detail=driver.find_element_by_css_selector('#top > main > div > div.layout__container > div.accordion__accordion > div > div').text
                fields['location_desc']=location_detail
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
                        #print(fields['lat'])
                        #print(fields['lng'])
                        map_lat[fields['location_name']]=lat
                        map_lng[fields['location_name']]=lng
                        print("Pass 3")
                        pass
                else:
                      fields['lat'] = map_lat[fields['location_name']]
                      fields['lng'] = map_lng[fields['location_name']]
                      
                
            except:
                print("error in  latlong.net")
                print(traceback.format_exc())
                
            
            
            
        except:
            print("location link name not found")
        
        #get start time with ticket link
        try:
            print("GEt ticket Link page:"+ticket_link)
            driver.get(ticket_link)
            google_id=''
            calendar=''
            twitter_id=''
            end_time=''
            if(ticket_link.find("ticketmaster.no")>=0):
                print("Ticket Master");
                start_time=driver.find_element_by_css_selector('#eventinfo > header > div.eventinfo__main__info > div > div.eventcard__body > div.eventcard__body__when').text
                start_time=str(start_time).split(",")[1]
                event_details=driver.find_element_by_css_selector("#main > script:nth-child(3)").text
                print("*********************************************")
                print("Event Details"+event_details)
                print("Start Time from ticket link:"+start_time)
                
            elif(ticket_link.find("ticketco")>=0):
                print("Ticket CO");
                start_time=driver.find_element_by_css_selector('#entity_44014 > div > aside > div:nth-child(2) > div.t-form-row > div:nth-child(1) > span:nth-child(4) > font > font').text
                start_time=str(start_time).split()[0]
                
                end_time=driver.find_element_by_css_selector("#entity_44014 > div > aside > div:nth-child(2) > div.t-form-row > div:nth-child(2) > font:nth-child(3) > font").text
                calendar=driver.find_element_by_css_selector("#entity_44014 > div > aside > div:nth-child(2) > div.text-center > a").get_attribute("href")
                calendar=driver.current_url+calendar
                google_id=driver.find_element_by_css_selector("#root > table > tbody > tr > td > a").get_attribute("href") 
                twitter_id=driver.find_element_by_css_selector("#b").get_attribute("href")
            elif(ticket_link.find("stavanger-konserthus.no")>0):
                print("stavanger-konserthus");
                start_time=driver.find_element_by_css_selector('#shows > tbody > tr > td:nth-child(3)').text
                start_time=str(start_time)
                
                end_time=driver.find_element_by_css_selector("#entity_44014 > div > aside > div:nth-child(2) > div.t-form-row > div:nth-child(2) > font:nth-child(3) > font").text
                calendar=driver.find_element_by_css_selector("#addeventatc1").get_attribute("href")
                twitter_id=driver.find_element_by_css_selector("#b").get_attribute("href")
            elif(ticket_link.find("folketeateret")>=0):
                print("folketeateret")
                start_time=driver.find_element_by_css_selector('#site-wrapper > div > div > div.small-6.medium-8.large-3.xlarge-2.columns.calendar-event__column.time > h5 > font > font').text
                start_time=str(start_time).split()[0]
                
            print("Start Time:"+start_time)
            fields['start_time']=start_time
            fields['google_id']=google_id
            fields['twitter_id']=twitter_id
            fields['end_time']=end_time
        
        except:
            print(traceback.format_exc())
            print("start time not found")
            print("getting start time from match event details")
            fields['start_time']=match_start
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
            
    
