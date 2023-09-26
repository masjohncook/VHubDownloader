#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Filename : msf_checker.py
@CreatedTime : 2023/09/26 21:05


This program has a function to __summary__

'''


############################################################################
# Import modules
############################################################################

import requests
from bs4 import BeautifulSoup
import json
import os
import argparse
import subprocess

############################################################################

__author__ = 'masjohncook'
__copyright__ = '(C)Copyright 2023'
__credits__ = []
__license__ = 'None'
__version__ = '0.0.1'
__maintainer__ = 'masjohncook'
__email__ = 'mas.john.cook@gmail.com'
__status__ = 'None'

############################################################################


def check_page(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    p = soup.find('p')
    
    if p:
        return True


def find_msf(link):
    msf_keyword = ['msf', 'metasploit', 'Metasploit', 'msfconsole']
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for keyword in msf_keyword:
        if keyword in soup.text:
            return keyword
        else:
            continue

def main():
    parser = argparse.ArgumentParser(description='check walkthrough link that contain Metasploit related terms')
    parser.add_argument('-j', '--json', required=True, help='Path to JSON file with VM names')
    args = parser.parse_args()
    number = 1
    result = []
    with open(args.json, 'r') as f:
        links = json.load(f)

    for link in links['wt_links']:
        
        print(f"{number}. Searching for {link}...")
        if check_page(link):
            print("That link has content")
        
        
        if find_msf(link):
            print("Has msf related content in {}".format(link))
            result.append(link)
            
        number += 1
    
    print(result)
    print(len(result))
    # with open(result.json, 'w') as r:
    #     json.dump(result, r, indent=4)
        

if __name__ == '__main__':
    main()