#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Filename : vulnhub_downloader.py
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

BASE_URL = "https://www.vulnhub.com"
SEARCH_URL = BASE_URL + "/?q={}&sort=date-asc&type=vm"

def get_vm_page_link(vm_name):
    search_page = requests.get(SEARCH_URL.format(vm_name))
    soup = BeautifulSoup(search_page.content, 'html.parser')
    div = soup.find('div', {'class': 'card-title'})
    link_element = div.a['href']
    print(link_element)
    if link_element:
        return BASE_URL + link_element
    return None

def get_download_link(vm_page_link):
    vm_page = requests.get(vm_page_link)
    soup = BeautifulSoup(vm_page.content, 'html.parser')
    div = soup.find('div', {'id': 'download'})
    for a in div.find_all('a', href=True):
        if 'download.vulnhub' in a['href']:
            link_element = a['href']

    if not link_element:
        pass
    else:
        return link_element
    return None

def download_file(url, output_dir):
    cmd = ["wget", "-nc", "-P", output_dir, url]
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description='Download .ova files from vulnhub.com')
    parser.add_argument('-j', '--json', required=True, help='Path to JSON file with VM names')
    parser.add_argument('-o', '--output', required=True, help='Output directory for .ova files')
    args = parser.parse_args()

    with open(args.json, 'r') as f:
        vm_names = json.load(f)

    for vm_name in vm_names['vm_name']:
        print(f"Searching for {vm_name}...")
        vm_page_link = get_vm_page_link(vm_name)
        if not vm_page_link:
            print(f"Could not find page for VM: {vm_name}")
            continue
        print(f"The page link is {vm_page_link}")
        print("--------------------------------")
        download_link = get_download_link(vm_page_link)
        
        if not download_link:
            print(f"Could not find download link for VM: {vm_name}")
            continue
        print("================================")
        print(f"Downloading {vm_name}...")
        download_file(download_link, args.output)
        print(f"{vm_name} downloaded!")
        print("================================")

if __name__ == '__main__':
    main()
