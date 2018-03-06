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
folder=dir_path+'/gdbillett.no'
csvfile = folder+'/gdbillett.no.csv'
try:
    if not os.path.exists(folder):
        os.makedirs(folder)
except:
    print("Folder Exist")
with open(csvfile, "w", encoding='utf-8') as output:
    writer = csv.writer(output, lineterminator='\n')
    if(page==0):
        writer.writerow(header)
    
for page in range(0,30,10):
    
    img_folder = folder + '/images'
    
    
    try:
        print(folder)
        os.mkdir(folder)
    except:
        print("Folder Exist")
    page_id=1
    next_page = 'https://www.gdbillett.no/arrangementer.aspx?q=&s='+str(page)
    print(next_page)
    print("================================")
    driver.get(next_page)
    sleep(2)
    #click for norway language
    main_window = driver.current_window_handle
    articles=driver.find_elements_by_css_selector('#ContentPlaceHolder1_ctlArrangementInfo > article')
    event_count=1
    count=0
    for article in articles:
        
        print("Count:"+str(count))
        count+=1
        event_link=article.find_element_by_css_selector('a').get_attribute('href')
        fields['site_scraped']=event_link
        print('Event Link:'+event_link)
        event_link='http://www.gdbillett.no/'+event_link
        try:
            ticket_link=article.find_element_by_css_selector('div > a').get_attribute('href')
            print("Ticket Link"+ticket_link)
            ticket_id_url=ticket_link[ticket_link.rfind('?')+1:]
            #print(ticket_id_url)
            event_id=ticket_id_url.split('&')[0].split('=')[1]
            #print(ticket_id_url.split('&'))
            #print(ticket_id_url.split('&')[0].split('='))
            arrangement_id=ticket_id_url.split('&')[1].split('=')[1]
            #print(arrangement_id)
            fields['ticket_link']=ticket_link
        except:
            print("Ticket Link not exist")
            #print(traceback.format_exc())
            
                
        #get to event_link website
        try:
            url=article.find_element_by_css_selector('div > h2 > a')
            url.send_keys(Keys.CONTROL+Keys.RETURN)
            driver.switch_to_window(driver.window_handles[1])
            sleep(1)
        except:
            print("Event Link not Present")
            print(traceback.format_exc())
        try:                
            image_link=driver.find_element_by_css_selector('#ContentPlaceHolder1_txtImgKode > p:nth-child(2) > img').get_attribute('src')
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
                    img_src = 'http://www.gdbillett.no/'+image_link
            
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
        
        try:
            event_name=driver.find_element_by_css_selector('#ContentPlaceHolder1_txtOverskriftKode > h1').text
            print("Event NAme:"+event_name)
            fields['event_name']=event_name
        except:
            print("Event Name not found")
            
        try:
            host_name=driver.find_element_by_css_selector('#ContentPlaceHolder1_txtOverlayKode2 > h3 > strong > a').text
            fields['host_name']=host_name
            print("Host name:"+host_name)
        except:
            print("Host not found")
        try:
            event_desc=driver.find_element_by_css_selector('#ContentPlaceHolder1_txtOverlayKode2 > p').text
            fields['event_desc']=event_desc
            print("Event Desc:"+event_desc)
            if(len(event_desc)==0):
                    event_desc=driver.find_element_by_css_selector('#ContentPlaceHolder1_txtOverlayKode2').text
                    fields['event_desc']=event_desc
                    print("Event Desc:"+event_desc)
        except:
            print("Event Desc not found")
            print(traceback.format_exc())
        
            
            
            
        #open the next ticket in current window
        
        try:
            if(len(ticket_link)>0):
                driver.get(ticket_link)
            else:
                raise ValueError('Ticket Link not found:'+ticket_link)
        
            #find last date
            try:
                event_rows=driver.find_elements_by_css_selector('#form1 > div.container > div > div.col-md-12.col-xs-12.col-sm-12 > div > div > div.table-responsive > table > tbody > tr')
                #print("Event Rows:"+str(len(event_rows)))
                if(len(event_rows)>2):
                    for i in range(1,len(event_rows)):
                        event_row=event_rows[i]
                        #print("Row number:"+str(i))
                        arr_id=event_row.find_element_by_css_selector('td:nth-child(1) > input[type="radio"]').get_attribute('value')
                        #print("Arr ID:"+arr_id)
                        if(arrangement_id==arr_id):
                             print("Arrangement ID===ARR ID")
                             start_time=event_row.find_element_by_css_selector('td:nth-child(2)').text
                             #print("Start Time:"+start_time)
                             fields['start_time'] = start_time
                             time_info=event_row.find_element_by_css_selector('td:nth-child(3)').text
                             #print("Time info:"+str(time_info))
                             #print("Time Split:"+str(time_info.split(',')))
                             time_date=time_info.split(',')[1]
                             
                             dt=parser.parse(time_date)
                             fields['start_date'] = str(dt.strftime('%d-%m-%Y')).split()[0]
                             last_event_row=driver.find_element_by_css_selector('#form1 > div.container > div > div.col-md-12.col-xs-12.col-sm-12 > div > div > div.table-responsive > table > tbody > tr:nth-child('+str(len(event_rows))+')')
                             time_info=driver.find_element_by_css_selector('#form1 > div.container > div > div.col-md-12.col-xs-12.col-sm-12 > div > div > div.table-responsive > table > tbody > tr:nth-child('+str(len(event_rows))+') > td:nth-child(3)').text
                             time_date=time_info.split(',')[1]
                             dt=parser.parse(time_date)
                             fields['end_date']= str(dt.strftime('%d-%m-%Y')).split()[0]
                             #fields['end_time']=fields['start_time']
                             fields['end_time']=''
                             #event_name
                             #fields['event_name']=driver.find_element_by_css_selector('td:nth-child(4)').text
                             #location_name
                             location_name=event_row.find_element_by_css_selector('td:nth-child(5)').text
                             fields['location_name']=location_name.strip()
                             print("Location name"+location_name)
                       
                            
                elif(len(event_rows)==2):
                     print("single event: ")
                     start_time=driver.find_element_by_css_selector('#form1 > div.container > div > div.col-md-12.col-xs-12.col-sm-12 > div > div > div.table-responsive > table > tbody > tr:nth-child(2) > td:nth-child(2)').text
                     fields['start_time'] = start_time
                     time_info=driver.find_element_by_css_selector('#form1 > div.container > div > div.col-md-12.col-xs-12.col-sm-12 > div > div > div.table-responsive > table > tbody > tr:nth-child(2) > td:nth-child(3)').text
                     time_date=time_info.split(',')[1]
                     dt=parser.parse(time_date)
                     fields['start_date'] = str(dt.strftime('%d-%m-%Y')).split()[0]
                     last_event_row=driver.find_element_by_css_selector('#form1 > div.container > div > div.col-md-12.col-xs-12.col-sm-12 > div > div > div.table-responsive > table > tbody > tr:nth-child('+str(len(event_rows))+')')
                     time_info=driver.find_element_by_css_selector('#form1 > div.container > div > div.col-md-12.col-xs-12.col-sm-12 > div > div > div.table-responsive > table > tbody > tr:nth-child('+str(len(event_rows))+') > td:nth-child(3)').text
                     time_date=time_info.split(',')[1]
                     dt=parser.parse(time_date)
                     fields['end_date']= str(dt.strftime('%d-%m-%Y')).split()[0]
                     #fields['end_time']=fields['start_time']
                     fields['end_time']=''
                     #event_name
                     #fields['event_name']=driver.find_element_by_css_selector('#form1 > div.container > div > div.col-md-12.col-xs-12.col-sm-12 > div > div > div.table-responsive > table > tbody > tr:nth-child(2) > td:nth-child(5)').text
                     #location_name
                     location_name=driver.find_element_by_css_selector('#form1 > div.container > div > div.col-md-12.col-xs-12.col-sm-12 > div > div > div.table-responsive > table > tbody > tr:nth-child(2) > td:nth-child(5)').text
                     fields['location_name']=location_name.strip()
                     #print("Location name"+location_name)
                else:
                    print("Date Error")
                     
            except:
                print("End Date Error")
                print(traceback.format_exc())
            
            #get latitute longitute and location
            #lat_lng
            try:
                if(fields['location_name'] not in map_lat or fields['location_name'] not in map_lng ):
                    print("Lat lng not saved in my map")
                    driver.get('https://www.latlong.net/')
                    inputEle = driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > input')
                    inputEle.send_keys(fields['location_name']+", Norway")
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
                        print("Pass 1")
                        pass
                else:
                    fields['lat'] = map_lat[fields['location_name']]
                    fields['lng'] = map_lng[fields['location_name']]
                        
            except:
                print("error in  latlong.net")
                print(traceback.format_exc())
            #get address from lat long
            if(len(str(fields['lng']).strip())>0 and len(str(fields['lat']).strip())>0 ):
                print("lat and lng exist"+str(fields['lat'])+" : "+str(fields['lng']))
                try:
                    if(fields['location_name'] not in map_addr):
                        print("location not  exists:")
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
                            textarea=driver.find_element_by_css_selector('#address')
                            location_address=textarea.get_attribute('value')
                            #print("location Address:"+location_address)
                            fields['location_address']=location_address.strip()
                            if(len(location_address.strip())>0):
                                map_addr[fields['location_name']]=location_address.strip()
                            print("Pass 2")
                            pass
                    else:
                        print("else location address exist:"+map_addr[fields['location_name']])
                        fields['location_address']=map_addr[fields['location_name']]
                except:
                    print("error in latlong address")
                    print(traceback.format_exc())
                    break;
        except:
            print("Ticket link invalid")
            driver.close()
            driver.switch_to_window(main_window)
            
            #driver.get(event_link)                
            #need to get all details from list page
            #need to do
            #get to event_link website
            
            try:
                location_name=article.find_element_by_css_selector('div > h3:nth-child(3) > a').text
                fields['location_name']=location_name
            except:
                print("location name not found")
            
            try:
                url=article.find_element_by_css_selector('a')
                url.send_keys(Keys.CONTROL+Keys.RETURN)
                driver.switch_to_window(driver.window_handles[1])
                sleep(1)
            except:
                print("Event Link not Present")
                print(traceback.format_exc())
            try:                
                image_link=driver.find_element_by_css_selector('#ContentPlaceHolder1_txtImgKode > p:nth-child(2) > img').get_attribute('src')
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
                        img_src = 'http://www.gdbillett.no/'+image_link
                
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
            
            try:
                event_name=driver.find_element_by_css_selector('#ContentPlaceHolder1_txtOverskriftKode > h1').text
                print("Event NAme:"+event_name)
                fields['event_name']=event_name
            except:
                print("Event Name not found")
                
            try:
                host_name=driver.find_element_by_css_selector('#ContentPlaceHolder1_txtOverlayKode2 > h3 > strong > a').text
                fields['host_name']=host_name
                print("Host name:"+host_name)
            except:
                print("Host not found")
            try:
                event_desc=driver.find_element_by_css_selector('#ContentPlaceHolder1_txtOverlayKode2 > p').text
                fields['event_desc']=event_desc
                print("Event Desc:"+event_desc)
                if(len(event_desc)==0):
                    event_desc=driver.find_element_by_css_selector('#ContentPlaceHolder1_txtOverlayKode2').text
                    fields['event_desc']=event_desc
                    print("Event Desc:"+event_desc)
                        
            except:
                print("Event Desc not found")
                print(traceback.format_exc())
                
            #get latitute longitute and location
            #lat_lng
            
            try:
                if(fields['location_name'] not in map_lat or fields['location_name'] not in map_lng ):
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
                        #print(fields['lat'])
                        #print(fields['lng'])
                        map_lat[fields['location_name']]=lat
                        map_lng[fields['location_name']]=lng
                        print("Pass 3")
                        pass
            except:
                print("error in  latlong.net")
                print(traceback.format_exc())
            #get address from lat long
            if(len(str(fields['lng']).strip())>0 and len(str(fields['lat']).strip())>0 ):
                try:
                    if(fields['location_name'] not in map_addr):
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
                            textarea=driver.find_element_by_css_selector('#address')
                            location_address=textarea.get_attribute('value')
                            #print("location Address:"+location_address)
                            fields['location_address']=location_address.strip()
                            if(len(location_address)>0):
                                map_addr[fields['location_name']]=location_address.strip()
                            print("Pass 4")
                            pass
                    else:
                        print("else location address exist:"+map_addr[fields['location_name']])
                        fields['location_address']=map_addr[fields['location_name']]
                except:
                    print("error in latlong address")
                    print(traceback.format_exc())
                    break;
            
                
             
            
            
        #fill details
        print("-------------Start----------------------")
        with open(csvfile, "a", encoding='utf-8') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(list(fields.values()))
            print("===================================================");
            print("===================================================");
            
            print("Count:"+str(event_count)+" Image:"+fields['image_name'])
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
            driver.close()
            driver.switch_to_window(main_window)
            #sleep(5)
            
            print("----------------End-------------------")
            
    else:
        print("Table header ")
        print("Pass 5")
        print("=======================")
        pass;