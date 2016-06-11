# -*- coding: utf-8 -*-
__author__ = 'Kambiz'

import sys
sys.path.insert(0, '/home/kambiz/itunes')
sys.path.insert(0, '/home/kambiz/itunes/app')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'itunes.settings'
import django
django.setup()

from bs4 import BeautifulSoup
import re
import datetime
import lxml.html
from app.models import *

def get_ranking(html_source, date, category):
    html = lxml.html.fromstring(html_source)

    rank_type='free'
    app_names=[]
    store_app_ids=[]
    ranks = range(1, len(html.xpath('//div[2]/table/tbody/tr/td[1]/div/div/span[1]/a'))+1 )
    for app_name in html.xpath('//div[2]/table/tbody/tr/td[1]/div/div/span[1]/a'):
        try:
            app_names.append(app_name.text[:150])
        except:
            app_names.append('NA')
    for store_app_id in html.xpath('//div[2]/table/tbody/tr/td[1]/div/div/span[3]'):
        try:
            store_app_ids.append(store_app_id.text)
        except:
            store_app_ids.append('NA')
    for rank, store_app_id, app_name in zip(ranks, store_app_ids, app_names):
        AppAnnieRankings.objects.create(store_app_id=store_app_id,
                                        app_name=app_name[:150],
                                        rank_type=rank_type,
                                        category=category[:150],
                                        rank=rank,
                                        date=date)

    rank_type='paid'
    app_names=[]
    store_app_ids=[]
    ranks = range(1, len(html.xpath('//div[2]/table/tbody/tr/td[2]/div/div/span[1]/a'))+1 )
    for app_name in html.xpath('//div[2]/table/tbody/tr/td[2]/div/div/span[1]/a'):
        try:
            app_names.append(app_name.text[:150])
        except:
            app_names.append('NA')
    for store_app_id in html.xpath('//div[2]/table/tbody/tr/td[2]/div/div/span[3]'):
        try:
            store_app_ids.append(store_app_id.text)
        except:
            store_app_ids.append('NA')
    for rank, store_app_id, app_name in zip(ranks, store_app_ids, app_names):
        AppAnnieRankings.objects.create(store_app_id=store_app_id,
                                        app_name=app_name[:150],
                                        rank_type=rank_type,
                                        category=category[:150],
                                        rank=rank,
                                        date=date)

    rank_type='grossing'
    app_names=[]
    store_app_ids=[]
    ranks = range(1, len(html.xpath('//div[2]/table/tbody/tr/td[3]/div/div/span[1]/a'))+1 )
    for app_name in html.xpath('//div[2]/table/tbody/tr/td[3]/div/div/span[1]/a'):
        try:
            app_names.append(app_name.text[:150])
        except:
            app_names.append('NA')
    for store_app_id in html.xpath('//div[2]/table/tbody/tr/td[3]/div/div/span[3]'):
        try:
            store_app_ids.append(store_app_id.text)
        except:
            store_app_ids.append('NA')
    for rank, store_app_id, app_name in zip(ranks, store_app_ids, app_names):
        AppAnnieRankings.objects.create(store_app_id=store_app_id,
                                        app_name=app_name[:150],
                                        rank_type=rank_type,
                                        category=category[:150],
                                        rank=rank,
                                        date=date)

    # soup = BeautifulSoup(html_source, 'html.parser')
    # count=0
    # for app in soup.findAll("td", {"class": "app"}):
    #     count += 1
    #     if count%3 == 1: #Free
    #         app_name = app.find('a').text
    #         store_app_id = app.find("span", {"style": "display:none"}).text
    #         rank_type = 'free'
    #     if count%3 == 2: #Paid
    #         app_name = app.find('a').text
    #         store_app_id = app.find("span", {"style": "display:none"}).text
    #         rank_type = 'paid'
    #     if count%3 == 0: #Grossing
    #         app_name = app.find('a').text
    #         store_app_id = app.find("span", {"style": "display:none"}).text
    #         rank_type = 'grossing'
    #     rank = ((count-0.1)//3)+1




from selenium import webdriver
from time import sleep

print 'Launching Firefox..'
browser = webdriver.Firefox()
print 'Entering to AppAnnie'
browser.get('https://www.appannie.com/account/login/')
print 'Waiting 5 seconds...'
sleep(3)

username = browser.find_element_by_id("email")
password = browser.find_element_by_id("password")
username.send_keys("kaminem64@yahoo.com")
password.send_keys("linux116")
browser.find_element_by_id("submit").click()

categories = ['books','business','catalogs','education','entertainment','finance','food-and-drink',
              'games','health-and-fitness','lifestyle','newsstand', 'medical','music','navigation','news','photo-and-video',
              'productivity','reference','shopping','social-networking','sports','travel','utilities','weather']

dates = ['2014-01-01', '2014-02-01', '2014-03-01', '2014-04-01', '2014-05-01', '2014-06-01', '2014-07-01', '2014-08-01',
         '2014-09-01', '2014-10-01', '2014-11-01', '2014-12-01', '2015-01-01', '2015-02-01', '2015-03-01', '2015-04-01',
         '2015-05-01', '2015-06-01', '2015-07-01', '2015-08-01', '2015-09-01', '2015-10-01', '2015-11-01', '2015-12-01',
         '2016-01-01']

for category in categories:
    for date in dates:
        url = 'https://www.appannie.com/apps/ios/top/united-states/'+category+'/?device=iphone&date='+date
        browser.get(url)
        try:
            browser.find_element_by_class_name("load-all").click()
        except:
            raw_input("Press Enter to continue...")
            url = 'https://www.appannie.com/apps/ios/top/united-states/'+category+'/?device=iphone&date='+date
            browser.get(url)
            browser.find_element_by_class_name("load-all").click()
        sleep(3)
        html_source = browser.page_source
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        get_ranking(html_source=html_source, date=date, category=category)

browser.close()
