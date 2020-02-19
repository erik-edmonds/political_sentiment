#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:04:59 2020

@author: erikedmonds

Twitter extraction for real time data feeds and sentiment analysis.
"""

import pycurl, re, os
from io import BytesIO, StringIO
from bs4 import BeautifulSoup
import pandas as pd

def curl(url,byte=False):
    if byte:
        buffer = BytesIO()
    else:
        buffer = StringIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEDATA, buffer)
    curl.perform()
    curl.close()
    file = buffer.getvalue()
    if type(file) == bytes:
        file = str(file)
    return file

def retrieve_files(directory, dump=False, path = '.'):
    if len(list(filter(lambda x: re.search(r'\w*[.]{1}csv', x) is not None, os.listdir(directory)))) != 7:
        text = curl(r'https://github.com/fivethirtyeight/data/blob/master/polls/README.md',True)
        soup = BeautifulSoup(text, 'html.parser')
        links = list(set(
                link.get('href') for link in soup.find_all('a') if 
                    re.search(r'[.]csv$', link.get('href')) is not None))
    dataframes=[pd.read_csv(link) for link in links]
    if not dump:
        return dataframes
    #d= {re.sub(r'[.]{1}csv','',re.split(r'/',item)[-1]):item for item in links}
    data= {re.split(r'/',item)[-1]:item for item in links}
    for key,value in zip(data.keys(),dataframes):
        value.to_csv(os.path.join(path,key),index=False)
    return

if __name__ == '__main__':
    try:
    #Makes sure there are 7 poll csv files 
        assert re.split(r'[\\/]{1}',os.getcwd())[-1].lower() == 'polls'
    except AssertionError:
        #subprocess.run(['git clone https://github.com/fivethirtyeight/data'], shell=True, capture_output=True)
        if os.path.isdir('polls'): pass
        else: 
            os.mkdir('polls')
        os.chdir('polls')