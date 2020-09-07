from bs4 import BeautifulSoup
import requests
import json

# https://eu-projekti.rs/category/ipa/
def crawl_eu_projekti(html, site):
    soup = BeautifulSoup(html, 'html.parser')

    posts = soup.findAll('div', {'class': 'post-row-center'})

    data = []

    for post in posts:
        title = post.a['title']
        url = post.a['href']
        text = ''
        for line in post.p.text.splitlines():
            text += line.strip()

        data.append({'site': site, 'title': title, 'description': text, 'url': url})

    return data


# http://www.kultura.gov.rs
def crawl_kultura_gov(html):
    soup = BeautifulSoup(html, 'html.parser')

    ul = soup.find(id='galleryListItems')
    posts = ul.findAll('li')

    data = []

    for post in posts:
        a = post.a
        href = a['href']
        title = a.text
        data.append({'site': 'http://www.kultura.gov.rs', 'title': title, 'url': 'http://www.kultura.gov.rs' + href})

    return data


# http://europa.rs/linkovi/eu-projekti-u-srbiji/
def crawl_europa(html):
    soup = BeautifulSoup(html, 'html.parser')

    content = soup.findAll('div', {'class': 'post-content'})[0]
    ul = content.ul
    posts = ul.findAll('li')

    data = []

    for post in posts:
        a = post.a
        href = a['href']
        title = a.text
        data.append({'site': 'http://europa.rs/linkovi/eu-projekti-u-srbiji/', 'title': title, 'url': href})
    
    return data


# crawl_eu_projekti
r1 = requests.get('https://eu-projekti.rs/category/ipa/')
r2 = requests.get('https://eu-projekti.rs/category/nacionalni-konkursi/')
r3 = requests.get('https://eu-projekti.rs/category/ostali-evropski-konkursi/')

# crawl_kultura_gov
r4 = requests.get('http://www.kultura.gov.rs/lat/konkursi/')

# crawl_europa
r5 = requests.get('http://europa.rs/linkovi/eu-projekti-u-srbiji/')

data1 = crawl_eu_projekti(r1.text, 'https://eu-projekti.rs/category/ipa/')
data2 = crawl_eu_projekti(r2.text, 'https://eu-projekti.rs/category/nacionalni-konkursi/')
data3 = crawl_eu_projekti(r3.text, 'https://eu-projekti.rs/category/ostali-evropski-konkursi/')

data4 = crawl_kultura_gov(r4.text)

data5 = crawl_europa(r5.text)

data = [*data1, *data2, *data3, *data4, *data5]

with open('data.json', 'w') as f:
    f.write(json.dumps(data, indent=4))