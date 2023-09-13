import requests
from bs4 import BeautifulSoup
import json
import os
import argparse
import subprocess


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
    # with open(result.json, 'w') as f:
    #     json.dump(result, f, indent=4)
        

if __name__ == '__main__':
    main()