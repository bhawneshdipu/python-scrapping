#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 01:10:34 2018

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
folder=dir_path+'/ringbillett.no'
csvfile = folder+'/ringbillett.no.csv'
try:
    if not os.path.exists(folder):
        os.makedirs(folder)
except:
    print("Folder Exist")
with open(csvfile, "w", encoding='utf-8') as output:
    writer = csv.writer(output, lineterminator='\n')
    if(page==0):
        writer.writerow(header)
    
for page in range(0,120,10):
    
    img_folder = folder + '/images'
    
    
    try:
        print(folder)
        os.mkdir(folder)
    except:
        print("Folder Exist")
    page_id=1
    next_page = 'https://www.ringbillett.no/arrangementer.aspx?q=&s='+str(page)
    print(next_page)
    print("================================")
    driver.get(next_page)
    sleep(2)
    #click for norway language
    main_window = driver.current_window_handle
    table_rows=driver.find_elements_by_css_selector('#ctl00_ContentPlaceHolder1_ctlArrangementInfo > center > table > tbody tr')
    for tr in table_rows:
        if(len(tr.find_elements_by_css_selector('td'))>1):
            event_link=tr.find_element_by_css_selector('td:nth-child(2) > a:nth-child(1)').get_attribute('href')
            fields['site_scraped']=event_link
            print('Event Link:'+event_link)
            try:
                ticket_link=tr.find_element_by_css_selector('td:nth-child(4) > a').get_attribute('href')
                print("Ticket Link"+ticket_link)
                event_link='http://www.ringbillett.no/'+event_link
                ticket_id_url=ticket_link[ticket_link.rfind('?')+1:]
                print(ticket_id_url)
                event_id=ticket_id_url.split('&')[0].split('=')[1]
                print(ticket_id_url.split('&'))
                print(ticket_id_url.split('&')[0].split('='))
                arrangement_id=ticket_id_url.split('&')[1].split('=')[1]
                print(arrangement_id)
                fields['ticket_link']=ticket_link
            except:
                print("Ticket Link not exist")
                print(traceback.format_exc())
                continue;
                
                
            #get to event_link website
            try:
                url=tr.find_element_by_css_selector('td:nth-child(2) > a:nth-child(1)')
                url.send_keys(Keys.CONTROL+Keys.RETURN)
                driver.switch_to_window(driver.window_handles[1])
            except:
                print("Event Link not Present")
                print(traceback.format_exc())
            try:                
                image_link=driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_ctlArrangementInfo > span:nth-child(1) > img').get_attribute('src')
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
                        img_src = 'http://www.ringbillett.no/'+image_link
                
                print("image src:"+img_src)
                x = img_src.split('/')[-1]
                print("x:"+x);
                fields['image_name']=x
                save_path = folder+"/"+x
                print("Save_path:"+save_path)
                if(len(img_src)>0):
                    urllib.request.urlretrieve(img_src, save_path)
            except Exception:
                print('no image')
                print(traceback.format_exc())
            
            try:
                event_name=driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_ctlArrangementInfo > span.infotabell-info1 > h1').text
                print("Event NAme:"+event_name)
                fields['event_name']=event_name
            except:
                print("Event Name not found")
            
            try:
                host_name=driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_ctlArrangementInfo > a').text
                fields['host_name']=host_name
            except:
                print("Host not found")
            try:
                event_desc=driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_ctlArrangementInfo > p').text
                fields['event_desc']=event_desc
            except:
                print("Event Desc not found")
                
            #open the next url in current window
            try:
                driver.get(ticket_link)
            
            
                #find last date
                try:
                    event_rows=driver.find_elements_by_css_selector('#Billett > table > tbody > tr')
                    print("Event Rows:"+str(len(event_rows)))
                    if(len(event_rows)>2):
                        for i in range(1,len(event_rows)):
                            event_row=event_rows[i]
                            print("Row number:"+str(i))
                            arr_id=event_row.find_element_by_css_selector('td:nth-child(1) > input[type="radio"]').get_attribute('value')
                            print("Arr ID:"+arr_id)
                            if(arrangement_id==arr_id):
                                 start_time=event_row.find_element_by_css_selector('td:nth-child(2)').text
                                 print("Start Time:"+start_time)
                                 fields['start_time'] = start_time
                                 time_info=event_row.find_element_by_css_selector('td:nth-child(3)').text
                                 print("Time info:"+str(time_info))
                                 print("Time Split:"+str(time_info.split(',')))
                                 time_date=time_info.split(',')[1]
                                 
                                 dt=parser.parse(time_date)
                                 fields['start_date'] = str(dt.strftime('%d-%m-%y')).split()[0]
                                 last_event_row=driver.find_element_by_css_selector('#Billett > table > tbody > tr:nth-child('+str(len(event_rows))+')')
                                 time_info=driver.find_element_by_css_selector('#Billett > table > tbody > tr:nth-child('+str(len(event_rows))+') > td:nth-child(3)').text
                                 time_date=time_info.split(',')[1]
                                 dt=parser.parse(time_date)
                                 fields['end_date']= str(dt.strftime('%d-%m-%y')).split()[0]
                                 #fields['end_time']=fields['start_time']
                                 fields['end_time']='23:30'
                                 #event_name
                                 #fields['event_name']=driver.find_element_by_css_selector('td:nth-child(4)').text
                                 #location_name
                                 location_name=driver.find_element_by_css_selector('td:nth-child(5)').text
                                 fields['location_name']=location_name
                                 print("Location name"+location_name)
                           
                                
                    elif(len(event_rows)==2):
                         print("single event: ")
                         start_time=driver.find_element_by_css_selector('#Billett > table > tbody > tr:nth-child(2) > td:nth-child(2)').text
                         fields['start_time'] = start_time
                         time_info=driver.find_element_by_css_selector('#Billett > table > tbody > tr:nth-child(2) > td:nth-child(3)').text
                         time_date=time_info.split(',')[1]
                         dt=parser.parse(time_date)
                         fields['start_date'] = str(dt.strftime('%d-%m-%y')).split()[0]
                         last_event_row=driver.find_element_by_css_selector('#Billett > table > tbody > tr:nth-child('+str(len(event_rows))+')')
                         time_info=driver.find_element_by_css_selector('#Billett > table > tbody > tr:nth-child('+str(len(event_rows))+') > td:nth-child(3)').text
                         time_date=time_info.split(',')[1]
                         dt=parser.parse(time_date)
                         fields['end_date']= str(dt.strftime('%d-%m-%y')).split()[0]
                         #fields['end_time']=fields['start_time']
                         fields['end_time']='23:30'
                         #event_name
                         #fields['event_name']=driver.find_element_by_css_selector('#Billett > table > tbody > tr:nth-child(2) > td:nth-child(5)').text
                         #location_name
                         location_name=driver.find_element_by_css_selector('#Billett > table > tbody > tr:nth-child(2) > td:nth-child(5)').text
                         fields['location_name']=location_name
                         print("Location name"+location_name)
                    else:
                        print("Date Error")
                        fields['start_time']=driver.find_element_by_css_selector('#Billett > table > tbody > tr:nth-child(2) > td:nth-child(2)').text
                        fields['start_date']=driver.find_element_by_css_selector('#Billett > table > tbody > tr:nth-child(2) > td:nth-child(3)').text.split(',')[1]
                        fields['end_date']=fields['start_date']
                        fields['end_time']='23:30'        
                except:
                    print("End Date Error")
                    print(traceback.format_exc())
                
                #get latitute longitute and location
                #lat_lng
                try:
                    if(fields['host_name'] not in map_lat or fields['host_name'] not in map_lng ):
                        driver.get('https://www.latlong.net/')
                        inputEle = driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > input')
                        inputEle.send_keys(fields['location_name']+', Norway')
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
                            map_lat[fields['host_name']]=lat
                            map_lng[fields['host_name']]=lng
                            pass
                except:
                    print("error in  latlong.net")
                    print(traceback.format_exc())
                #get address from lat long
                
                try:
                    if(fields['location_name']+', Norway' not in map_addr):
                        driver.get('https://www.latlong.net/Show-Latitude-Longitude.html')
                        lat_input=driver.find_element_by_xpath("//input[@placeholder='lat']")
                        lat_input.send_keys(fields['lat'])
                        lng_input=driver.find_element_by_xpath("//input[@placeholder='long']")
                        lng_input.send_keys(fields['lng'])
                        #click get
                        driver.find_element_by_css_selector('body > main > div.row > div.col-7.graybox > form > div.row > div:nth-child(3) > button').click()
                        sleep(1)
                        try:
                            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                                           'Timed out waiting for PA creation ' +
                                                           'confirmation popup to appear.')
                            alert = driver.switch_to.alert
                            alert.accept()
                            print("alert accepted")
                        except TimeoutException:
                            #sleep(5)
                            print("no alert")
                            location_address=driver.find_element_by_css_selector('#address').get_attribute("innerText")
                            print("location Address:"+location_address)
                            location_address=driver.find_element_by_css_selector('#address').text
                            print("location Address:"+location_address)
                            textarea=driver.find_element_by_css_selector('#address')
                            location_address=textarea.get_attribute('value')
                            print("location Address:"+location_address)
                            fields['location_address']=location_address
                            if(len(location_address)>0):
                                map_addr[fields['location_name']+', Norway']=location_address
                                location_address=driver.find_element_by_css_selector('#address').text
                            pass
                    else:
                        print("else location address:"+map_addr[fields['location_name']+', Norway'])
                        fields['location_address']=map_addr[fields['location_name']+', Norway']
                except:
                    print("error in latlong address")
                    print(traceback.format_exc())
                    break;
            except:
                print("Ticket link invalid")
                #need to get all details from event link
                #need to do
             
            
            
            #fill details
            with open(csvfile, "a", encoding='utf-8') as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerow(list(fields.values()))
                fields = fields.fromkeys(fields, '')
                sleep(1)
                driver.close()
                driver.switch_to_window(main_window)
                print("================================")
                
        else:
            print("Table header ")
            pass;
