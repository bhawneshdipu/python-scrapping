# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 03:01:26 2018

@author: aptus
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

def month_to_num(name):
    if name == "jan": return '01'
    elif name == "feb": return '02'
    elif name == "mar": return '03'
    elif name == "apr": return '04'
    elif name == "may": return '05'
    elif name == "jun": return '06'
    elif name == "jul": return '07'
    elif name == "aug": return '08'
    elif name == "sep": return '09'
    elif name == "oct": return '10'
    elif name == "nov": return '11'
    elif name == "dec": return '12'
    else: raise 'valueerror'

fields= OrderedDict([('ai_id', ''),
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
('whatsapp_id', '')])

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
#cities=['Alta', 'Arendal', 'Askim', 'Bergen', 'Bodø', 'Brekstad', 'Brevik', 'Brumunddal', 'Bryne', 'Brønnøysund', 'Drammen', 'Drøbak', 'Egersund', 'Elverum', 'Fagernes', 'Farsund', 'Fauske', 'Finnsnes', 'Flekkefjord', 'Florø', 'Fosnavåg', 'Fredrikstad', 'Førde', 'Gjøvik', 'Grimstad', 'Halden', 'Hamar', 'Hammerfest', 'Harstad', 'Haugesund', 'Hokksund', 'Holmestrand', 'Honningsvåg', 'Horten', 'Hønefoss', 'Jessheim', 'Jørpeland', 'Kirkenes', 'Kolvereid', 'Kongsberg', 'Kongsvinger', 'Kopervik', 'Kragerø', 'Kristiansand', 'Kristiansund', 'Langesund', 'Larvik', 'Leirvik', 'Leknes', 'Levanger', 'Lillehammer', 'Lillesand', 'Lillestrøm', 'Lyngdal', 'Mandal', 'Mo i Rana', 'Molde', 'Mosjøen', 'Moss', 'Mysen', 'Måløy', 'Namsos', 'Narvik', 'Notodden', 'Odda', 'Orkanger', 'Oslo', 'Otta', 'Porsgrunn', 'Risør', 'Rjukan', 'Sandefjord', 'Sandnes', 'Sandnessjøen', 'Sandvika', 'Sarpsborg', 'Sauda', 'Ski', 'Skien', 'Skudeneshavn', 'Sortland', 'Stathelle', 'Stavanger', 'Stavern', 'Steinkjer', 'Stjørdalshalsen', 'Tananger', 'Tromsø', 'Trondheim', 'Tvedestrand', 'Tønsberg', 'Ulsteinvik', 'Vadsø', 'Vardø', 'Verdalsøra', 'Vinstra', 'Åkrehamn', 'Ålesund', 'Åndalsnes']
#cities=['Halden', 'Hamar']
#cities=['Odda']
#cities=['Vinstra', 'Verdalsøra', 'Vardø', 'Vadsø', 'Ulsteinvik', 'Tønsberg', 'Tvedestrand', 'Trondheim', 'Tromsø', 'Tananger', 'Stjørdalshalsen', 'Steinkjer', 'Stavern', 'Stavanger', 'Stathelle', 'Sortland', 'Skudeneshavn', 'Skien', 'Ski', 'Sauda', 'Sarpsborg', 'Sandvika', 'Sandnessjøen', 'Sandnes', 'Sandefjord', 'Rjukan', 'Risør', 'Porsgrunn', 'Otta', 'Oslo', 'Orkanger', 'Odda', 'Notodden', 'Narvik', 'Namsos', 'Måløy', 'Mysen', 'Moss', 'Mosjøen', 'Molde', 'Mo i Rana', 'Mandal']
#cities=['Mandal', 'Mo i Rana', 'Molde', 'Mosjøen', 'Moss', 'Mysen', 'Måløy', 'Namsos', 'Narvik', 'Notodden', 'Odda', 'Orkanger', 'Oslo', 'Otta', 'Porsgrunn', 'Risør', 'Rjukan', 'Sandefjord', 'Sandnes', 'Sandnessjøen', 'Sandvika', 'Sarpsborg', 'Sauda', 'Ski', 'Skien', 'Skudeneshavn', 'Sortland', 'Stathelle', 'Stavanger', 'Stavern', 'Steinkjer', 'Stjørdalshalsen', 'Tananger', 'Tromsø', 'Trondheim', 'Tvedestrand', 'Tønsberg', 'Ulsteinvik', 'Vadsø', 'Vardø', 'Verdalsøra', 'Vinstra']
#cities=['Åndalsnes']
#cities=['Bergen', 'Bodø', 'Brekstad', 'Brevik', 'Brumunddal', 'Bryne', 'Brønnøysund']

#cities=['Drammen','Drøbak']
#cities=['Egersund','Elverum']
#cities=['Fagernes','Farsund','Fauske','Finnsnes','Flekkefjord',
#cities=['Florø','Førde','Fosnavåg']#
#cities=['Fredrikstad','Gjøvik','Grimstad']
#cities=['Langesund','Larvik','Leirvik','Leknes','Levanger','Lillehammer','Lillesand','Lillestrøm','Lyngdal']
#cities=['Oslo','Otta','Porsgrunn','Risør','Rjukan']
#cities=['Tananger','Tønsberg','Tromsø','Trondheim','Tvedestrand','Ulsteinvik','Vadsø','Vardø','Verdalsøra','Vinstra']
#cities=['Steinkjer','Stjørdalshalsen']
#cities=['Fauske']
#cities=['Fosnavåg']
#cities=['Larvik']
cities=['Lillehammer']
cities=['Gjøvik']
header = list(fields.keys())
city_id=1
for city in cities:
    
    folder=dir_path+'/data/'+str(city)
    img_folder = folder + '/images'
    
    
    try:
        print(folder)
        os.mkdir(folder)
    except:
        print("Folder Exist")
    page_id=1
    next_city = 'https://ebillett.no/events?page='+str(page_id)+'&search='+city
    driver.get(next_city)
    sleep(2)
    #click for norway language
    if(city_id==1):
        driver.find_element_by_css_selector('#dx-navbar-collapse > ul > li:nth-child(1) > a').click()
    sleep(2)
    main_window = driver.current_window_handle
    
    csvfile = folder+'/'+str(city)+'.csv'
    with open(csvfile, "w", encoding='utf-8') as output:
        writer = csv.writer(output, lineterminator='\n')
        if(page_id==1):
            writer.writerow(header)
    while True:
        containers = driver.find_elements_by_css_selector('#pjax-event-list-result-container > div.container')
        nth_child = len(containers)
        print([city,nth_child])
        event_links = driver.find_elements_by_css_selector('#pjax-event-list-result-container > div:nth-child('+str(nth_child+1)+') > div#events-list > ul.event-box-wide.container > li.row > div.event-title > a')
        total_events = len(event_links)
        print(total_events)
        
        if total_events > 0:
            row_id=1
            for event in event_links:
                print(event.get_attribute('href'))
                event.send_keys(Keys.CONTROL + Keys.RETURN)
                driver.switch_to_window(driver.window_handles[1])
                sleep(1)
                
                #click to get english language for date time
                driver.find_element_by_css_selector('#dx-navbar-collapse > ul > li:nth-child(1) > a').click()
                #get time info
                try:
                    
                    time_info = driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div:nth-child(2) > div > div:nth-child(1) > div.media-body').text
                    split_raw = time_info.split('\n')
                    print(split_raw)
                    #for start date time
                    tmp_sdt = str.replace(split_raw[0].split(',',1)[1].strip(),',','').split(' ')
                    print(tmp_sdt)
                    print(tmp_sdt[0][0:3])
                    day=tmp_sdt[1].strip()
                    if(len(day) ==1):
                        day='0'+day
                    fields['start_date'] = day+ '-' + month_to_num(tmp_sdt[0][0:3].lower().strip()) + '-' + tmp_sdt[2].strip()
                    fields['start_time'] = tmp_sdt[3].strip()
                    
                    #for end time
                    fields['end_time'] = re.search('\d\d:\d\d', split_raw[1]).group()
                    #calculation end date
                    stime = datetime.datetime.strptime(fields['start_time'], '%H:%M')
                    etime = datetime.datetime.strptime(fields['end_time'], '%H:%M')
                    if etime > stime:
                        print('=====================================End time is on the same day')
                        fields['end_date'] = fields['start_date']
                    else:
                        sdate = datetime.datetime.strptime(fields['start_date'], '%d-%m-%Y')
                        edate = sdate + datetime.timedelta(days=1)
                        fields['end_date'] = datetime.datetime.strftime(edate, '%d-%m-%Y')
                        print('====================================End time is on other day :: ' + fields['end_date'])
                    
                except Exception:
                    print('Date time error')
                    print(traceback.format_exc())
                    
                #click back for norway language for rest data extraction
                driver.find_element_by_css_selector('#dx-navbar-collapse > ul > li:nth-child(1) > a').click()
                
                #event_name
                fields['event_name']=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div.row.p-30 > div.col-md-24.col-sm-16.col-xs-16 > h1').text
                print(fields['event_name'])
                
                #download image
                try:
                    img_src = driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-6.col-md-8.col-sm-24.col-xs-24.hidden-sm.hidden-xs > div.row.p-20 > div > img').get_attribute('src')
                    print(img_src)
                    x = str.replace(img_src,'?width=260','').rsplit('/',1)[1]
                    print(x);
                    fields['image_name']=x
                    save_path = folder+'/'+x
                    print(save_path)
                    urllib.request.urlretrieve(img_src, save_path)
                except Exception:
                    print('no image')
                
                #ticket_link
                try:
                    fields['ticket_link']=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-6.col-md-8.col-sm-24.col-xs-24.hidden-sm.hidden-xs > div.panel.panel-default.p-10 > div > div > div:nth-child(3) > a').get_attribute('href')
                except:
                    try:
                        fields['ticket_link']=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-6.col-md-8.col-sm-24.col-xs-24.hidden-sm.hidden-xs > div.panel.panel-default.p-10 > div > div > div > a').get_attribute('href')
                    except:
                        fields['ticket_link']=''
                        print('no ticket')
                    
                #event_desc
                event_desc=''
                try:
                    event_desc=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div.panel.panel-default.synopsis.p-10 > div').text
                except Exception:
                    print("no event details")
                try:
                    event_desc= event_desc+'\n'+driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div:nth-child(5) > div').text
                except Exception:
                    try:
                        event_desc = event_desc+'\n'+driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div:nth-child(4) > div').text
                    except Exception:
                        print('no event details')
                    print("no event details")
                
                fields['event_desc'] = event_desc
                #print(fields['event_desc']) 
                
                #for other elements
                route = driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div:nth-child(2) > div > div:nth-child(3) > div.media-body.clearfix > div.pull-right.more-events-from.hidden-xs > a').get_attribute('href')
                driver.get(route)
                
                #host_name
                try:
                    fields['host_name'] = driver.find_element_by_css_selector('#section-content > div.page-header.partner-page-header > div > h1').text
                except Exception:
                    print('no host name')
                print(fields['host_name'])
                
                if fields['host_name'] not in host_map:
                    #location_name
                    fields['location_name'] = fields['host_name']
                    
                    #location_address
                    try:
                        fields['location_address']= fields['location_name'] + ' '+ driver.find_element_by_css_selector('#section-content > div.page-header.partner-page-header > div > address').text
                    except Exception:
                        fields['location_address']=''
                        print('no location address')
                    print(fields['location_address'])
                    
                    #website
                    try:
                        website = driver.find_element_by_css_selector('#section-content > div.page-header.partner-page-header > div > ul > li:nth-child(2) > a')
                        fields['website'] = website.get_attribute('href')
                        print(fields['website'])
                    except:
                        print('no websites')
                    
                    #lat_lng
                    driver.get('https://www.latlong.net/')
                    inputEle = driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > input')
                    inputEle.send_keys(fields['location_address'])
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
                        pass
                    host_map[fields['host_name']] = [fields['location_name'], fields['location_address'], fields['lat'], fields['lng'], fields['website']]
                else:
                    value = host_map[fields['host_name']]
                    fields['location_name'] = value[0]
                    fields['location_address'] = value[1]
                    fields['lat']=value[2]
                    fields['lng']=value[3]
                    fields['website']=value[4]
                fields['city'] = city
                with open(csvfile, "a", encoding='utf-8') as output:
                    writer = csv.writer(output, lineterminator='\n')
                    writer.writerow(list(fields.values()))
                fields = fields.fromkeys(fields, '')
                sleep(1)
                driver.close()
                driver.switch_to_window(main_window)
                print("=====================city_id :: "+ str(city_id)+" page :: " + str(page_id) + " / " + str(row_id) + " / " + str(total_events))
                fields = fields.fromkeys(fields, '')
                row_id = row_id + 1
            page_id = page_id + 1
            next_page = 'https://ebillett.no/events?page='+ str(page_id) +'&search='+city
            driver.get('https://ebillett.no/events?page='+ str(page_id) +'&search='+city)
            main_window = driver.current_window_handle
            sleep(2)
            continue
        else:
            print('no data for city. going to next city')
            break
            #start to write
    city_id=city_id+1
    #click to get english language for date time
    #driver.find_element_by_css_selector('#dx-navbar-collapse > ul > li:nth-child(1) > a').click()
    #sleep(3)
    print(city_id)
