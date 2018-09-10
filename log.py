# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import base64
import random
from time import sleep
import datetime


url = "http://deliveryportal.icicibankltd.com/UI/Login.aspx"
url = "http://deliveryportal.icicibankltd.com/"
charArray = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '', 'Ç', 'ü', 'é', 'â', 'ä', 'à', 'å', 'ç', 'ê', 'ë', 'è', 'ï', 'î', 'ì', 'Ä', 'Å', 'É', 'æ', 'Æ', 'ô', 'ö', 'ò', 'û', 'ù', 'ÿ', 'Ö', 'Ü', 'ø', '£', 'Ø', '×', 'ƒ', 'á', 'í', 'ó', 'ú', 'ñ', 'Ñ', 'ª', 'º', '¿', '®', '¬', '½', '¼', '¡', '«', '»', '_', '_', '_', '¦', '¦', 'Á', 'Â', 'À', '©', '¦', '¦', '+', '+', '¢', '¥', '+', '+', '-', '-', '+', '-', '+', 'ã', 'Ã', '+', '+', '-', '-', '¦', '-', '+', '¤', 'ð', 'Ð', 'Ê', 'Ë', 'È', 'i', 'Í', 'Î', 'Ï', '+', '+', '_', '_', '¦', 'Ì', '_', 'Ó', 'ß', 'Ô', 'Ò', 'õ', 'Õ', 'µ', 'þ', 'Þ', 'Ú', 'Û', 'Ù', 'ý', 'Ý', '¯', '´', '¬', '±', '_', '¾', '¶', '§', '÷', '¸', '°', '¨', '•', '¹', '³', '²', '_', ' ']

def enc(pwd, hdnE, hdnN, hdnD):
    newpwd = ""
    for c in pwd:
        if newpwd == "":
            newpwd = ((charArray.index(c)+32) ** hdnE) % hdnN
        else:
            newpwd = str(newpwd) + "/" + str(((charArray.index(c)+32) ** hdnE) % hdnN)
    return newpwd
def login(ban,oPass,soup):
  
    
    _eventargument=""
    
    try:
        _eventargument = soup.find('input', {'id': '_EVENTARGUMENT'}).get('value')
    except:
        pass
    
    __eventtarget=""
    
    try:
        __eventtarget = soup.find('input', {'id': '__EVENTTARGET'}).get('value')
    except:
        pass
    
    
    __lastfocus=""
    
    try:
        __lastfocus = soup.find('input', {'id': '__LASTFOCUS'}).get('value')
    except:
        pass
    
    __viewstate =""
    
    try:
        __viewstate = soup.find('input', {'id': '__VIEWSTATE'}).get('value')
    except:
        pass
    
    hdnD=""
    
    try:
        hdnD = soup.find('input', {'id': 'hdnD'}).get('value')
        hdnD = int(hdnD)
    except:
        pass
    
    hdnE=""
    
    try:
        hdnE = soup.find('input', {'id': 'hdnE'}).get('value')
        hdnE = int(hdnE)
    except:
        pass
    
    hdnN=""
    
    try:
        hdnN = soup.find('input', {'id': 'hdnN'}).get('value')
        hdnN = int(hdnN)
    except:
        pass
    
    txtRemarks="Login"
    
    try:
        txtRemarks = soup.find('input', {'id': 'txtRemarks'}).get('value')
    except:
        pass
    if txtRemarks == None:
       txtRemarks = "Login" 
    
    nPass = enc(oPass,hdnE,hdnN,hdnD)
    
    payload={ 
            "__EVENTARGUMENT": _eventargument,
            "__EVENTTARGET":__eventtarget,
            "__LASTFOCUS":__lastfocus,
            "__VIEWSTATE":__viewstate,
            "btnLogin":"Login",
            "hdnD":hdnD,
            "hdnE":hdnE,
            "hdnN":hdnN,
            "txtLoginID":ban,
            "txtPassword":nPass,
            "txtRemarks":txtRemarks
            }
    
    headers = {
        'origin': "http://deliveryportal.icicibankltd.com",
        'upgrade-insecure-requests': "1",
        'content-type': "application/x-www-form-urlencoded",
        'user-agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'referer': "http://deliveryportal.icicibankltd.com/UI/Login.aspx",
        'accept-encoding': "gzip, deflate",
        'accept-language': "en-US,en;q=0.9",
        'cache-control': "no-cache"
        }
    
    print(hdnE)
    print(hdnN)
    print(hdnD)
    print(oPass)
    print(nPass)
    print(payload)
    print(headers)
    response = s.post(url, data=payload, headers=headers)
    
    print(response.status_code)
    
    resp_home = s.get("http://deliveryportal.icicibankltd.com/UI/Home.aspx?RND="+str(random.randint(3000000, 9999999)))
    
    soup = BeautifulSoup(resp_home.content, "html.parser")
        
    #print(resp_home.text)
    print(resp_home.status_code)
    message=""
    try:
        message = soup.find(id='ctl00_AS_TopHeader1_lblUserName',text=True).text
        time = soup.find(id='ctl00_AS_TopHeader1_lblLoginTime',text=True).text
        print("Message::"+str(message))
        print("Time::"+str(time))
        
    except:
        try:
            message = soup.find(id="lblMessage").text
            print("Message::"+str(message))
        except:
            pass
    
    file = open("out.txt", "w")
    file.write(resp_home.text)
    file.close()

    return s,resp_home



if __name__=="__main__":
    rnd=random.randint(1,28)
    dt=datetime.datetime.now()
    
    if dt.minute>rnd:
        rnd=dt.minute+1
    
    while True:
        dt=datetime.datetime.now()
        print(str(rnd)+"   "+str(dt.minute))
        if dt.minute==rnd:
            print("++++++++++++")
            ban = str(base64.b64decode(b'QkFOMTIyNzQy'),"utf-8")
            oPass = str(base64.b64decode(b'aGFkb29wXzI='),"utf-8")
            s = requests.Session()
            r = s.get("http://deliveryportal.icicibankltd.com")
            soup = BeautifulSoup(r.content, "html.parser")
            print(r.status_code)
            s,resp = login(ban,oPass,soup)
            break
        else:
            sleep(29)
    
    
    

