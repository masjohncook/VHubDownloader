import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://www.vulnhub.com'
TIMELINE_URL = 'https://www.vulnhub.com/timeline/'

def get_vm_links_from_timeline():
    link_list = []
    response = requests.get(TIMELINE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', {'class': 'span12 well'})
    all_a = div.find_all('a')
    for a in all_a:
        name = a.text
        href = a.get('href')
        link = BASE_URL+href
        link_list.append([name, link])
    
    return link_list
    # vm_name = div.a.contents
    # vm_link = div.a['href']
    # print("{} : {}{}".format(vm_name, BASE_URL, vm_link))
    # return vm_name, vm_link
    # Inspect the page to find the exact selector. This is hypothetical.
    

def main():
    results = get_vm_links_from_timeline()

    with open('all_link_lists.json', 'w') as f:
        json.dump(results, f, indent=4)
    
if __name__ == '__main__':
    main()