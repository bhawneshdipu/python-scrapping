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
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(dir_path+'/chromedriver',chrome_options=chromeOptions)
#driver = webdriver.Chrome(dir_path+'/chromedriver')

social_link = dir_path+'/social_link.csv'
header = ['ai_id', 'category', 'event_name', 'event_desc', 'start_date', 'start_time', 'end_date', 'end_time', 'host_name', 'location_name', 'location_address', 'location_desc', 'host_contact', 'lat', 'lng', 'city', 'ticket_link', 'facebookhost_id', 'website', 'facebook_id', 'linkedin_id', 'twitter_id', 'instagram_id', 'pinterest_id', 'google_id', 'skype_id', 'youtube_id', 'discord_id', 'snapchat_id', 'ello_id', 'periscope_id', 'vimeo_id', 'meerkat_id', 'vine_id', 'flickr_id', 'tumblr_id', 'medium_id', 'tripadvisor_id', 'dribble_id', 'whatsapp_id']


div_file = dir_path+'/div_count'
div_file_cnt = 0
with open(div_file) as f: 
    for line in f: 
        div_file_cnt = int(line)
print(div_file_cnt)
div_count = 1;

page_file = dir_path+'/page_count'
page_file_cnt = 0
with open(page_file) as f: 
    for line in f: 
        page_file_cnt = int(line)
print(page_file_cnt)
page_count = 1;


next_url = 'https://trdevents.no/events/list/?tribe_event_display=list&tribe-bar-date=2018-03-01'

while True:
    driver.get(next_url)
    if page_count < page_file_cnt:
        page_count = page_count + 1
        print('Moving to page :: '+ str(page_count));
        next_url = driver.find_element_by_css_selector('#tribe-events-footer > li.nav-link.next-link > a').get_attribute('href')
        continue
    else:
        print('**************************************');
    
    eventDivs = driver.find_elements_by_css_selector('#tribe-events-content > div.tribe-events-loop.vcalendar > div')
    totalDivs = len(eventDivs)
    print(totalDivs);
    
    csvfile = dir_path+'/scrape_'+str(page_count)+'.csv'
    with open(csvfile, "a") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(header)
    
    main_window = driver.current_window_handle
    
    for div in eventDivs:
        try:
            #start_date
            '''month = div.find_element_by_css_selector('div > div.col-event-date.col-sm-2.hidden-xs > div > div > p.calendar-month').text
            day = div.find_element_by_css_selector('div > div.col-event-date.col-sm-2.hidden-xs > div > div > p.calendar-day').text
            year = '2018'
            start_date = day+'-'+month+'-'+year
            print(start_date)'''
            if(div_count < div_file_cnt and div_count != 1):
                div_count = div_count+1
                continue
            
            
            
            url = ''
            url = div.find_element_by_css_selector('div > div.col-event-content.col-sm-6.hidden-xs > h2 > a')
            url_value = url.get_attribute('href')
            print(url_value)
            url.send_keys(Keys.CONTROL + Keys.RETURN)
            driver.switch_to_window(driver.window_handles[1])
            sleep(2)
            
            #event_name
            event_name = driver.find_element_by_css_selector('#tribe-events-content > h2').text
            print(event_name)
            
            #event_desc
            event_desc = driver.find_element_by_css_selector('.tribe-events-single-event-description.tribe-events-content.entry-content.description').text
            event_desc = " ".join(event_desc.split())
            print(event_desc)
            
            #start_date
            sdate = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.primary.tribe-clearfix > div:nth-child(1) > dl > dd:nth-child(2) > abbr').get_attribute('title')
            dt = parse(sdate)
            start_date = dt.strftime('%d/%m/%Y')
            print(start_date)
            
            #start_time
            stime = ''
            start_time =''
            end_date=''
            end_time=''
            try:
                stime = driver.find_element_by_css_selector('#tribe-events-content > div.tribe-events-schedule.updated.published.tribe-clearfix > div > h3 > span.tribe-event-date-start').text
                start_time = stime.split('@')[1].strip()
                print(start_time)
                
                #end_date
                end_date=start_date
                print(end_date)
                
                #end_time
                end_time = driver.find_element_by_css_selector('#tribe-events-content > div.tribe-events-schedule.updated.published.tribe-clearfix > div > h3 > span.tribe-event-date-end').text
                print(end_time)
            except:
                start_time = '00.00'
                end_date = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.primary.tribe-clearfix > div:nth-child(1) > dl > dd:nth-child(4) > abbr').get_attribute('title')
                end_time = '23.59'
                pass
                    
            
            
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
            vimeo_id=''
            try:
                tmp = driver.find_element_by_css_selector('div.tribe-events-single-section.tribe-events-event-meta.primary.tribe-clearfix > div:nth-child(2) > dl').text
                x = tmp.split('\n')
                print(x)
                J=0
                while(J<len(x)):
                    with open(social_link, "a") as output:
                        writer = csv.writer(output, lineterminator='\n')
                        writer.writerow([x[J], url_value])
                        
                    if not website and "mer info" in x[J].lower():
                        website = x[J+1]
                        print(website + '-->mer info added to website<--')
                    if  "facebook" in x[J].lower():
                        if "/events/" in x[J+1].lower():
                            facebook_id = x[J+1]
                        else:
                            facebookhost_id = x[J+1]
                    if "billett-link" in x[J].lower():
                        ticket_link = x[J+1]
                    if "video-link" in x[J].lower():
                        vimeo_id= x[J+1]
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
                WebDriverWait(driver, 2).until(EC.alert_is_present(),
                                               'Timed out waiting for PA creation ' +
                                               'confirmation popup to appear.')
            
                alert = driver.switch_to.alert
                #print(alert.accept())
                print("alert accepted")
            except TimeoutException:
                print("no alert")
                lat=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div > input').get_attribute('value')
                lng=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div:nth-child(2) > input').get_attribute('value')
                lat = str(lat)
                lng = str(lng)
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
            meerkat_id=''
            vine_id=''
            flickr_id=''
            tumblr_id=''
            medium_id=''
            tripadvisor_id=''
            dribble_id=''
            whatsapp_id=''
            
            final_list = [ai_id, category, event_name, event_desc, start_date, start_time, end_date, end_time, host_name, location_name, location_address, location_desc, host_contact, lat, lng, city, ticket_link, facebookhost_id, website, facebook_id, linkedin_id, twitter_id, instagram_id, pinterest_id, google_id, skype_id, youtube_id, discord_id, snapchat_id, ello_id, periscope_id, vimeo_id, meerkat_id, vine_id, flickr_id, tumblr_id, medium_id, tripadvisor_id, dribble_id, whatsapp_id]
            
            with open(csvfile, "a") as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerow(final_list)
            
            print('============================================Page:: '+str(page_count)+' Div:: '+str(div_count)+' / '+str(totalDivs)+' complete')
            print('')
            sleep(1)
            driver.close()
            driver.switch_to_window(main_window)
            #break
            div_count = div_count + 1
            
            with open(div_file, "w") as f: 
                f.write(str(div_count))
        except Exception:
            print('no data here')
            if not url:
                print('THIS DIV CONTAINS ADS')
                continue
            else:
                print(traceback.format_exc())
                break
    next_url = driver.find_element_by_css_selector('#tribe-events-footer > li.nav-link.next-link > a').get_attribute('href')
    
    page_count = page_count + 1
    div_count = 1
    with open(page_file, "w") as f: 
        f.write(str(page_count))
#close chrome driver
driver.close()