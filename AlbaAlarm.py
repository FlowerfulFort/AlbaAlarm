from bs4 import BeautifulSoup
import win32api
import os
import sys
# import urllib.request as rq
import requests
import configparser
import time
# import threading
import signal
from plyer import notification

def signal_handle(sig, frame):
    ExitAlertThrow('Ctrl+C received.. exit the program.')
    sys.exit()

def InitialSettingINI():
    if (not os.path.isfile('setting.ini')):
        newfile = configparser.ConfigParser()
        newfile['WebConfig'] = {}
        # URL for Crawling
        newfile['WebConfig']['WebURL'] = ''
        # Rate for refreshing web session (Seconds)
        newfile['WebConfig']['RefreshRate'] = '0'
        
        with open('setting.ini', 'w') as f:
            newfile.write(f)
def ExitAlertThrow(msg):
    win32api.MessageBox(0, msg, 'AlbaAlarm')
    sys.exit()

# Set signal handler(Ctrl+C)
signal.signal(signal.SIGINT, signal_handle)

# Check if setting file exists
if (not os.path.isfile('setting.ini')):
    InitialSettingINI()
    ExitAlertThrow('Please edit setting.ini file for program to run...')

# Read config file
config = configparser.ConfigParser()
config.read('setting.ini')
webconf = config['WebConfig']

# Open Kakao Session & AlbaCheunkuk URL
s = requests.session()
url = requests.get(webconf['weburl'])

if (not url.ok) or (webconf['refreshrate'] == 0):
    ExitAlertThrow('Please write correct URL or refreshrate to setting.ini...')

bs = BeautifulSoup(url.text, 'html.parser')

oldFirstTable = bs.select_one('tr.firstLine')
newFirstTable = ''
count = 0   # for loop counting
print('now : {0}'.format(oldFirstTable.select_one('span.title').text))
while True:
    time.sleep(int(webconf['refreshrate']))
    url = requests.get(webconf['weburl'])
    bs = BeautifulSoup(url.text, 'html.parser')
    newFirstTable = bs.select_one('tr.firstLine')

    if(not oldFirstTable.select_one('span.title') == newFirstTable.select_one('span.title')):
        print('Count : {0}, {1}'.format(count, newFirstTable.select_one('span.title').text))
        notification.notify(
            title = newFirstTable.select_one('span.company').text,
            message = '{albaTitle}\n{place}'.format(albaTitle=newFirstTable.select_one('span.title').text, place=newFirstTable.select_one('td.local > div').text),
            timeout = 5
        )
        oldFirstTable = newFirstTable
    count+=1