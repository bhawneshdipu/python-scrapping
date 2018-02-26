#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 21:37:06 2018

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

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(dir_path+'/chromedriver',chrome_options=chromeOptions)
#driver.add_cookie({'ebillett_locale'='no', 'expires'='', 'path'='/'})
cities=['Åkrehamn','Ålesund','Alta','Åndalsnes','Arendal','Askim','Bergen','Bodø','Brekstad','Brevik','Brønnøysund','Brumunddal','Bryne','Drammen','Drøbak','Egersund','Elverum','Fagernes','Farsund','Fauske','Finnsnes','Flekkefjord','Florø','Førde','Fosnavåg','Fredrikstad','Gjøvik','Grimstad','Halden','Hamar','Hammerfest','Harstad','Haugesund','Hokksund','Holmestrand','Hønefoss','Honningsvåg','Horten','Jessheim','Jørpeland','Kirkenes','Kolvereid','Kongsberg','Kongsvinger','Kopervik','Kragerø','Kristiansand','Kristiansund','Langesund','Larvik','Leirvik','Leknes','Levanger','Lillehammer','Lillesand','Lillestrøm','Lyngdal','Måløy','Mandal','Mo i Rana','Molde','Mosjøen','Moss','Mysen','Namsos','Narvik','Notodden','Odda','Orkanger','Oslo','Otta','Porsgrunn','Risør','Rjukan','Sandefjord','Sandnes','Sandnessjøen','Sandvika','Sarpsborg','Sauda','Ski','Skien','Skudeneshavn','Sortland','Stathelle','Stavanger','Stavern','Steinkjer','Stjørdalshalsen','Tananger','Tønsberg','Tromsø','Trondheim','Tvedestrand','Ulsteinvik','Vadsø','Vardø','Verdalsøra','Vinstra']
cities=['Odda']
pageid=1
done=0
url='https://ebillett.no/events?search='
for city in cities:
    try:
        folder=dir_path+'/'+str(city)
        csvfile = folder+'/ebillrtt.no_'+str(pageid)+'.csv'
        try:
            os.mkdir(folder)
        except:
            print("Folder Exist")
        header = ['ai_id', 'category', 'event_name', 'event_desc', 'start_date', 'start_time', 'end_date', 'end_time', 'host_name', 'location_name', 'location_address', 'location_desc', 'host_contact', 'lat', 'lng', 'city', 'ticket_link', 'facebookhost_id', 'website', 'facebook_id', 'linkedin_id', 'twitter_id', 'instagram_id', 'pinterest_id', 'google_id', 'skype_id', 'youtube_id', 'discord_id', 'snapchat_id', 'ello_id', 'periscope_id', 'vimeo_id', 'meerkat_id', 'vine_id', 'flickr_id', 'tumblr_id', 'medium_id', 'tripadvisor_id', 'dribble_id', 'whatsapp_id']
        
        with open(csvfile, "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            if(done==0):
                writer.writerow(header)
            
            print('https://ebillett.no/events?search='+city)
            driver.get('https://ebillett.no/events?search='+city)
            main_window = driver.current_window_handle
            #dx-navbar-collapse > ul > li:nth-child(1) > a
            sleep(3)
            driver.find_element_by_css_selector('#dx-navbar-collapse > ul > li:nth-child(1) > a').click()
            sleep(3)
            #eventDivs = driver.find_elements_by_css_selector('#events-list > ul.event-box-wide.container')
            eventTypeContainer = driver.find_elements_by_css_selector('#pjax-event-list-result-container > .container')
            
            
            print('Container: '+str(len(eventTypeContainer)))
            i=0
            netid=0
            for eventType in eventTypeContainer:
                main_window = driver.current_window_handle
            
                try:
                    if(i<=done):
                        continue;
                    tagList=eventType.find_element_by_css_selector('div#events-list > ul.event-box-wide.container ')
                    tagList=tagList.find_elements_by_css_selector('.row')
                    time=''
                    for tagEle in tagList:
                        #time
                            
                        print(tagEle.tag_name);
                        try:
                            if(tagEle.tag_name=='div'):
                                time=tagEle.text
                                if(len(time)==0):
                                    time=tagEle.get_attribute("innerText")
                        except:
                            print("Time Div not Found")
                            pass;
                        
            
                        if(tagEle.tag_name=='li'):
                            #event_link
                            event_link=tagEle.find_element_by_css_selector('div.event-title.col-sm-8.col-xs-24.vcenter > a').get_attribute('href')
                            event_link_ele=tagEle.find_element_by_css_selector('div.event-title.col-sm-8.col-xs-24.vcenter > a')
                            
                            #event_name
                            event_name=tagEle.find_element_by_css_selector('div.event-title.col-sm-8.col-xs-24.vcenter > a > h4').text
                            #event_location
                            event_location=tagEle.find_element_by_css_selector('div.location.col-sm-6.col-xs-24.vcenter > span.event-promoter > a').text
                            #event_location_link
                            event_location_link=tagEle.find_element_by_css_selector('div.location.col-sm-6.col-xs-24.vcenter > span.event-promoter > a').get_attribute('href')
                            event_location_link_ele=tagEle.find_element_by_css_selector('div.location.col-sm-6.col-xs-24.vcenter > span.event-promoter > a')
   
                            #event_address
                            event_location_address=tagEle.find_element_by_css_selector('div.location.col-sm-6.col-xs-24.vcenter > span.event-location').text                                             
                            print("Time->:"+time)
                            print("Event Link->:"+event_link)
                            print("Event Name->:"+event_name)
                            print("Event Location->:"+event_location)
                            print("Event Location Link->:"+event_location_link)
                            
                            print("Event Location Address->:"+event_location_address)
                            
                            
                            #open event website:
                            print("opening event window:::"+event_link)
                            
                            url=event_link_ele
                            url.send_keys(Keys.CONTROL+Keys.RETURN)
                            driver.switch_to_window(driver.window_handles[1])
                            sleep(2) #seconds
                            
                            driver.get(event_link)
                            time=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div:nth-child(2) > div > div:nth-child(1) > div.media-body').text
                            #sleep(3)
                            driver.find_element_by_css_selector('#dx-navbar-collapse > ul > li:nth-child(1) > a').click()
                            sleep(3)
            
                            event_name=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div.row.p-30 > div > h1').text
                            start_date=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div:nth-child(2) > div > div:nth-child(1) > div.media-body > h4').text
                            #process start date for time
                            end_time_str=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div:nth-child(2) > div > div:nth-child(1) > div.media-body').text
                            ticket_link=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-6.col-md-8.col-sm-24.col-xs-24.hidden-sm.hidden-xs > div.panel.panel-default.p-10 > div > div > div:nth-child(3) > a').get_attribute('href')
                            #event desc
                            event_desc=''
                            event_image=''
                            try:
                                event_desc_elements=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div.panel.panel-default.synopsis.p-10 > div')
                                '''for desc_ele in event_desc_elements:
                                    event_desc+=str(desc_ele.text)
                                    '''
                                event_desc=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div.panel.panel-default.synopsis.p-10 > div').text
                                print(event_desc+"--------------------->")
                                event_details=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-18.col-md-16.col-sm-24.col-xs-24 > div:nth-child(5) > div').text
                                event_desc+=" "+event_details
                                event_image=driver.find_element_by_css_selector('#section-content > div.container.events-details > div > div.col-lg-6.col-md-8.col-sm-24.col-xs-24.hidden-sm.hidden-xs > div.row.p-20 > div > img').get_attribute('src')
                                print("Image:"+event_image)
                                if(len(event_image)>0):
                                    # download the image
                                    urllib.request.urlretrieve(event_image, folder+'/'+event_image)
                                    #urllib.urlretrieve(event_image, folder+'/images_'+event_image)
                            except:
                                pass;
                            
                            print(event_name,start_date,end_time_str,event_desc,event_image)
                            print("back to window:::")
                                                        
                            #open location website:
                                
                            print("opening location window:::"+event_location_link)
                
                            driver.get(event_location_link)
                            location_name=driver.find_element_by_css_selector('#section-content > div.page-header.partner-page-header > div > h1').text
                            location_address=driver.find_element_by_css_selector('#section-content > div.page-header.partner-page-header > div > address').text
                            promoter_website=driver.find_element_by_css_selector('#section-content > div.page-header.partner-page-header > div > ul > li:nth-child(2) > a').get_attribute('href')
                            
                            print(location_name,location_address,promoter_website)

                            #open promoter website:
                                
                            print("opening location window:::"+promoter_website)
                
                            driver.get(promoter_website)
                            host_name=driver.find_element_by_css_selector('head > title').text
                            
                            print("Host Name:"+host_name)

                            
                            print("back to window:::")
                            
                            #latitute and longitude
                            
                            print("opening latlong window:::")
                            driver.switch_to_window(driver.window_handles[1])
                            sleep(2) #seconds
                
                            driver.get('https://www.latlong.net/')
                            inputEle = driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > input')
                            inputEle.send_keys(event_location)
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
                                #print(alert.accept())
                                print("alert accepted")
                            except TimeoutException:
                                print("no alert")
                                print(traceback.format_exc())
                                lat=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div > input').get_attribute('value')
                                lng=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div:nth-child(2) > input').get_attribute('value')
                                print(lat)
                                print(lng)
                                
                            
                                    #sleep(1) 
                                #driver.switch_to_window(main_window)
                                print("back to  main window")
                                driver.close();
                                driver.switch_to_window(main_window)
                                pass
                            
                            
                            #final Data
                            ai_id=''
                            category=''
                            event_name=event_name
                            event_desc=event_desc
                            start_date=start_date
                            
                            start_time=time[str.rfind(time,'.')+1:]
                            end_time=end_time_str[str.rfind(end_time_str,'.')+1:]
                            host_name=''
                            location_name=location_name
                            end_date=''
                            host_name=''
                            location_name=location_name
                            location_address=location_address
                            location_desc=''
                            host_contact=''
                            lat=lat
                            lng=lng
                            city=city
                            ticket_link=ticket_link
                            facebookhost_id=''
                            website=''
                            facebook_id=''
                            linkedin_id=''
                            twitter_id=''
                            instagram_id=''
                            pinterest_id=''
                            google_id=''
                            skype_id=''
                            youtube_id=''
                            discord_id=''
                            snapchat_id=''
                            ello_id=''
                            periscope_id=''
                            vimeo_id=''
                            meerkat_id=''
                            vine_id=''
                            flickr_id=''
                            tumblr_id=''
                            medium_id=''
                            tripadvisor_id=''
                            dribble_id=''
                            whatsapp_id=''
                            
                            header = ['ai_id', 'category', 'event_name', 'event_desc', 'start_date', 'start_time', 'end_date', 'end_time', 'host_name', 'location_name', 'location_address', 'location_desc', 'host_contact', 'lat', 'lng', 'city', 'ticket_link', 'facebookhost_id', 'website', 'facebook_id', 'linkedin_id', 'twitter_id', 'instagram_id', 'pinterest_id', 'google_id', 'skype_id', 'youtube_id', 'discord_id', 'snapchat_id', 'ello_id', 'periscope_id', 'vimeo_id', 'meerkat_id', 'vine_id', 'flickr_id', 'tumblr_id', 'medium_id', 'tripadvisor_id', 'dribble_id', 'whatsapp_id']
                            final_data=[ai_id,category,event_name,event_desc,start_date,start_time,end_date,end_time,host_name,location_name,location_address,location_desc,host_contact,lat,lng,city,ticket_link,facebookhost_id,website,facebook_id,linkedin_id,twitter_id,instagram_id,pinterest_id,google_id,skype_id,youtube_id,discord_id,snapchat_id,ello_id,periscope_id,vimeo_id,meerkat_id,vine_id,flickr_id,tumblr_id,medium_id,tripadvisor_id,dribble_id,whatsapp_id]                         
                            
                            writer.writerow(final_data)
                            
                            i=i+1
                            print(i)
                            print('=============================================:'+str(i))
                            print("Time:"+time);
                            #break
                                
                except Exception:
                    print('No Event Data')
                    #continue;
                    driver.switch_to_window(driver.window_handles[0])
                    print(traceback.format_exc())
                    continue;
                    #events-list > ul.event-box-wide.container > li > div.promoter-title.col-sm-8.col-xs-24.vcenter > a
                    '''try:
                        location_link=eventType.find_element_by_css_selector('#events-list > ul.event-box-wide.container > li > div.promoter-title.col-sm-8.col-xs-24.vcenter > a').get_attribute('href')
                        print("Promoter Location Link:"+location_link)
                        #open location website:
                        website_window = driver.current_window_handle
                           
                        driver.get(event_location_link)
                        location_name=driver.find_element_by_css_selector('#section-content > div.page-header.partner-page-header > div > h1').text
                        location_address=driver.find_element_by_css_selector('#section-content > div.page-header.partner-page-header > div > address').text
                        promoter_website=driver.find_element_by_css_selector('#section-content > div.page-header.partner-page-header > div > ul > li:nth-child(2) > a').get_attribute('href')
                        driver.switch_to_window(website_window)

                        website_window = driver.current_window_handle
                           
                        #latitute and longitude
                        driver.get('https://www.latlong.net/')
                        inputEle = driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > input')
                        inputEle.send_keys(event_location)
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
                            #print(alert.accept())
                            print("alert accepted")
                        except TimeoutException:
                            print("no alert")
                            lat=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div > input').get_attribute('value')
                            lng=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div:nth-child(2) > input').get_attribute('value')
                            print(lat)
                            print(lng)
                            pass
                        
                                #sleep(1) 
                            #driver.switch_to_window(main_window)
                            website_window = driver.current_window_handle
                           
                            #break
                    except:
                        print('No Event and Promoter Data')
                    #print(traceback.format_exc())
                    '''
    except:
        print("Exception Occurs")
        print(traceback.format_exc())
                
driver.close()
