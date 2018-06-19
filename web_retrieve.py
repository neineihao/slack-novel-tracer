from bs4 import BeautifulSoup
import requests
import logging

def get_page(req_url):
    headers = {"User-Agent":
                   "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) "
                   "AppleWebKit/536.26 (KHTML, like Gecko) "
                   "Version/6.0 Mobile/10A5376e Safari/8536.25",
               }
    logging.debug("Connecting: {}".format(req_url))
    r = requests.get(req_url, headers=headers)
    return r.text

def update_get(url, odd_index):
    return_list = []
    page = get_page(url)
    soup = BeautifulSoup(page, "html.parser")
    for li in soup.findAll('li'):
        for a in li.findAll('a'):
            test = a.get('href')
            index = int(test.split('.')[0])
            if index > odd_index:
                content = a.contents[0].split()
                chapter = content[0][1:-1]
                try:
                    return_list.append((index, chapter, content[1]))
                except:
                    continue
    return return_list

if __name__ == '__main__':
    url = "https://www.piaotian.com/html/6/6760/index.html"
    update = update_get(url, 6478632)
    for i in update:
        print(i)
