# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 02:42:28 2018

@author: aptus
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 23:20:14 2018

@author: aptus
"""
import os
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

cities=['Åkrehamn','Ålesund','Alta','Åndalsnes','Arendal','Askim','Bergen','Bodø','Brekstad','Brevik','Brønnøysund','Brumunddal','Bryne','Drammen','Drøbak','Egersund','Elverum','Fagernes','Farsund','Fauske','Finnsnes','Flekkefjord','Florø','Førde','Fosnavåg','Fredrikstad','Gjøvik','Grimstad','Halden','Hamar','Hammerfest','Harstad','Haugesund','Hokksund','Holmestrand','Hønefoss','Honningsvåg','Horten','Jessheim','Jørpeland','Kirkenes','Kolvereid','Kongsberg','Kongsvinger','Kopervik','Kragerø','Kristiansand','Kristiansund','Langesund','Larvik','Leirvik','Leknes','Levanger','Lillehammer','Lillesand','Lillestrøm','Lyngdal','Måløy','Mandal','Mo i Rana','Molde','Mosjøen','Moss','Mysen','Namsos','Narvik','Notodden','Odda','Orkanger','Oslo','Otta','Porsgrunn','Risør','Rjukan','Sandefjord','Sandnes','Sandnessjøen','Sandvika','Sarpsborg','Sauda','Ski','Skien','Skudeneshavn','Sortland','Stathelle','Stavanger','Stavern','Steinkjer','Stjørdalshalsen','Tananger','Tønsberg','Tromsø','Trondheim','Tvedestrand','Ulsteinvik','Vadsø','Vardø','Verdalsøra','Vinstra']
pageid=1
done=0
    for(cty in cities):
    csvfile = dir_path+'ebillett_no-'+str(city)+'.csv'
    social_link = dir_path+'/social_link.csv'
    header = ['ai_id', 'category', 'event_name', 'event_desc', 'start_date', 'start_time', 'end_date', 'end_time', 'host_name', 'location_name', 'location_address', 'location_desc', 'host_contact', 'lat', 'lng', 'city', 'ticket_link', 'facebookhost_id', 'website', 'facebook_id', 'linkedin_id', 'twitter_id', 'instagram_id', 'pinterest_id', 'google_id', 'skype_id', 'youtube_id', 'discord_id', 'snapchat_id', 'ello_id', 'periscope_id', 'vimeo_id', 'meerkat_id', 'vine_id', 'flickr_id', 'tumblr_id', 'medium_id', 'tripadvisor_id', 'dribble_id', 'whatsapp_id']
    with open(csvfile, "a") as output:
        writer = csv.writer(output, lineterminator='\n')
        if(done==0):
            writer.writerow(header)
        
    for pageid in range(32,33):
            
        #driver.get('https://trdevents.no/events/list/?tribe_event_display=list&tribe-bar-date=2018-03-01')
        driver.get('https://trdevents.no/events/list/?tribe_paged='+str(pageid)+'&tribe_event_display=list&tribe-bar-date=2018-03-01')
        eventDivs = driver.find_elements_by_css_selector('#tribe-events-content > div.tribe-events-loop.vcalendar > div')
        
        print(len(eventDivs))
        
        main_window = driver.current_window_handle
        i=0
        netid=0
        for div in eventDivs:
            try:
                i=i+1
                if(i<=done):
                    continue;
                #start_date
                '''month = div.find_element_by_css_selector('div > div.col-event-date.col-sm-2.hidden-xs > div > div > p.calendar-month').text
                day = div.find_element_by_css_selector('div > div.col-event-date.col-sm-2.hidden-xs > div > div > p.calendar-day').text
                year = '2018'
                start_date = day+'-'+month+'-'+year
                print(start_date)'''
                print(i)
                print(div.get_attribute('id'))
                print(str(div.get_attribute('id')).find('netboard'));
                if(str(div.get_attribute('id')).find('netboard')>=0):
                    continue;
                try:
                    url = div.find_element_by_css_selector('div > div.col-event-content.col-sm-6.hidden-xs > h2 > a')
                except:
                    print('Exception  in URL element not found')
                    url = div.find_element_by_css_selector('div >  div.col-event-content.col-xs-12.visible-xs > h2 > a')
                
                print ("URL to open: "+url.get_attribute('href'))
                #sleep(3)
                print ("URL opened: "+url.get_attribute('href'))
                url.send_keys(Keys.CONTROL+Keys.RETURN)
                driver.switch_to_window(driver.window_handles[1])
                sleep(2) #seconds
                #event_name
                
                try:
                    event_name = driver.find_element_by_css_selector('#tribe-events-content > h2').text
                except:
                    print('Exception  in Event Name')
                    sleep(2)
                    event_name = driver.find_element_by_css_selector('#tribe-events-content > h2').text
                
                #event_name = driver.find_element_by_css_selector('#tribe-events-content > h2').text
                print("Event Name:"+event_name)
                
                #event_desc
                event_desc = driver.find_element_by_css_selector('.tribe-events-single-event-description.tribe-events-content.entry-content.description').text
                event_desc = " ".join(event_desc.split())
                print("Event Desc:"+event_desc)
                
                #start_date
                sdate = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.primary.tribe-clearfix > div:nth-child(1) > dl > dd:nth-child(2) > abbr').get_attribute('title')
                dt = parse(sdate)
                start_date = dt.strftime('%d/%m/%Y')
                print("Start Date:"+start_date)
                
                #start_time
                stime = driver.find_element_by_css_selector('#tribe-events-content > div.tribe-events-schedule.updated.published.tribe-clearfix > div > h3 > span.tribe-event-date-start').text
                if(len(stime.split('@'))>=2):
                    start_time = stime.split('@')[1].strip()
                    print("Start Time: "+start_time)
                        
                    #end_date
                    edate = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.primary.tribe-clearfix > div:nth-child(1) > dl > dd:nth-child(4) > abbr').get_attribute('title')
                
                    end_date=edate
                    print("End Date: "+end_date)
                    
                    #end_time
                    end_time = driver.find_element_by_css_selector('#tribe-events-content > div.tribe-events-schedule.updated.published.tribe-clearfix > div > h3 > span.tribe-event-date-end').text
                    print("End Time: "+end_time)
                else:
                    category = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.primary.tribe-clearfix > div:nth-child(1) > dl > dd:nth-child(6) > a').text
                    if(str(category).lower().find('festival')):
                        start_time='00.00'                        
                        print("Start Time:: "+start_time)
                        end_time='23.59'
                        print("End Time:: "+end_time)
                start_time=start_time.replace('.','.');
                end_time=end_time.replace('.','.');
                
                #host_name
                host_name = ''
                try :
                    host_name = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.primary.tribe-clearfix > div.tribe-events-meta-group.tribe-events-meta-group-organizer > dl > dd.tribe-organizer').text.strip()
                    print(host_name)
                except Exception:
                    #print(traceback.format_exc())
                    print ('--no host_name')
                    pass
                
                #location_name
                location_name = ''
                try :
                    location_name = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.secondary.tribe-clearfix > div.tribe-events-meta-group.tribe-events-meta-group-venue > dl > dd.tribe-venue > a').text
                    print(location_name)
                except Exception:
                    #print(traceback.format_exc())
                    print ('--no location_name')
                    pass
                
                #location_address
                location_address = ''
                try:
                    location_address = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.secondary.tribe-clearfix > div.tribe-events-meta-group.tribe-events-meta-group-venue > dl > dd.tribe-venue-location > address > span').text
                    #location_address = string.replace(location_address, '\n', ' ')  
                    location_address = " ".join(location_address.split())
                    print(location_address)
                except Exception:
                    #print(traceback.format_exc())
                    print ('--no location_address')
                    pass
                
                #host_contact
                host_contact=''
                try:
                    host_contact = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.primary.tribe-clearfix > div.tribe-events-meta-group.tribe-events-meta-group-organizer > dl > dd.email').text
                    print(host_contact)
                except Exception:
                    #print(traceback.format_exc())
                    print ('--no host_contact')
                    pass
                
                #city
                city='Trondheim'
                print(city)
                
                #extra info
                #website
                website = ''
                try:
                    website = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.primary.tribe-clearfix > div.tribe-events-meta-group.tribe-events-meta-group-organizer > dl > dd.url > a').get_attribute('href')
                    print(website)
                except Exception:
                    #print(traceback.format_exc())
                    print ('--no website')
                    pass
                
                #fb_id, fb_event, booking link
                facebookhost_id = ''
                facebook_id = ''
                ticket_link = ''
                try:
                    tmp = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.primary.tribe-clearfix > div:nth-child(2) > dl').text
                    x = tmp.split('\n')
                    print(x)
                    J=0
                    while(J<len(x)):
                        with open(social_link, "a") as output:
                            writer = csv.writer(output, lineterminator='\n')
                            writer.writerow(x[J])
                        if not website and "mer info" in x[J].lower():
                            website = x[J]
                        if  "facebook" in x[J].lower():
                            if "/events/" in x[J+1].lower():
                                facebook_id = x[J+1]
                            else:
                                facebookhost_id = x[J+1]
                        if "billett-link" in x[J].lower():
                            ticket_link = x[J+1]
                        J=J+2
                    print(facebookhost_id)
                    print(facebook_id)
                    print(ticket_link)
                except Exception:
                    #print(traceback.format_exc())
                    print ('--no check manually')
                    pass
                
                driver.get('https://www.latlong.net/')
                inputEle = driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > input')
                inputEle.send_keys(location_address)
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
                
                #less used values
                ai_id=''
                category=''
                location_desc=''
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
                
                final_list = [ai_id, category, event_name, event_desc, start_date, start_time, end_date, end_time, host_name, location_name, location_address, location_desc, host_contact, lat, lng, city, ticket_link, facebookhost_id, website, facebook_id, linkedin_id, twitter_id, instagram_id, pinterest_id, google_id, skype_id, youtube_id, discord_id, snapchat_id, ello_id, periscope_id, vimeo_id, meerkat_id, vine_id, flickr_id, tumblr_id, medium_id, tripadvisor_id, dribble_id, whatsapp_id]
                print("Final List:")
                print(final_list)
                with open(csvfile, "a") as output:
                    writer = csv.writer(output, lineterminator='\n')
                    writer.writerow(final_list)
                
                print('============================================')
                print('')
                sleep(1)
                driver.close()
                #sleep(1)
                driver.switch_to_window(main_window)
                #break
            except Exception:
                print('no data here')
                print(traceback.format_exc())
                break
        #close chrome driver
driver.close()
