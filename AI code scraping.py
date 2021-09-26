import os
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd

chrome_driver_path = 'path'
UserUsername = 'UserUsername'
UserPassword = 'UserPassword'
domain_index_start = domain_index_start 
domain_index_end = domain_index_end
chromedriver = (chrome_driver_path)

os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get('http://auction.whois.ai/users/login/home')
emailElem = driver.find_element_by_id('UserUsername')
emailElem.send_keys(UserUsername)
passwordElem = driver.find_element_by_id('UserPassword')
passwordElem.send_keys('UserPassword')
apasswordElem.submit()


output = pd.DataFrame(columns = ['Amount','bidder','Date','Domain'])

for i in range(domain_index_start,domain_index_end):
    successful = 0
    while successful == 0:
        try:
            time.sleep(3)
            url = 'http://auction.whois.ai/bids/index/' + str(i)
            driver.get(url)
            all_spans = driver.find_elements_by_xpath("/html/body/div[2]/div/table/tbody")
            for span in all_spans:
                l = span.text
            dname = driver.find_elements_by_xpath("/html/body/div[2]/div/h1/a")
            for span in dname:
                dn = span.text

            tem = pd.DataFrame(l.split("\n"),columns=['temp'])
            tem = pd.DataFrame(tem.temp.str.split(' ',2).tolist(),columns = ['Amount','bidder','Date'])
            tem['Domain'] = str(dn)
            was = ['Amount','User','Date']
            for i in was:
                tem = tem.replace(i,"")
                
            output = pd.concat([output,tem])
            print('Iter Coint : '+ str(i))

            #Highest bidder 
            output.sort_values(by=['Amount'],ascending=False).drop_duplicates(subset=['Domain']).to_csv(r'Highest_bidder.csv')
            output.to_csv(r'Bidder_Log.csv')
            successful = 1
        except Exception as e:
            print('Retrying')
            
