import requests
from bs4 import BeautifulSoup
import time
import json

mainUrl = 'https://www.4icu.org/de/universities/'
baseUrl = 'https://www.4icu.org'

response = requests.get(mainUrl)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')


tables = soup.find('table', class_='table')
stateLinks = []

for aTag in tables.find_all('a', href=True):
    stateName = aTag.text.strip()
    stateUrl = baseUrl + aTag['href']
    stateLinks.append({'state name': stateName, 'state url': stateUrl})


for state in stateLinks:
    print(f"State: {state['state name']}, URL: {state['state url']}")

print(f"Total {len(stateLinks)} states")


stateUniversities = []
for state in stateLinks:
    url = state['state url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    uni_table = soup.find('tbody')
    universityLinks = []

    for aTag in uni_table.find_all('a', href=True):
        if aTag['href'] == '/about/add.htm':
            continue
        uniUrl = baseUrl + aTag['href']
        universityLinks.append(uniUrl)
    stateUniversities.append({'state': state['state name'], 'universityLinks': universityLinks})


universities = []
for university in stateUniversities:
    stateName = university['state']
    for uniUrl in university['universityLinks']:
        response = requests.get(uniUrl)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')


        logo = soup.find('img', attrs={"itemprop": "logo"})
        uniName = soup.find('h1', attrs={"itemprop": "name"})
        cityName = soup.find('span', attrs={"itemprop": "addressLocality"})
        type = soup.find('p', class_='lead').find('strong')
        foundedYear = soup.find('table', class_='table borderless').find('span', attrs={"itemprop": "foundingDate"})
        socialLinks = soup.find('div', attrs={"id": "social-media"}).find_all('a', attrs={"itemprop": "sameAs"})
        uniLink = soup.find('a', attrs={"itemprop": "url"})


        def determine_media_type(url):
            if 'facebook.com' in url:
                return 'facebook'
            elif 'instagram.com' in url:
                return 'instagram'
            elif 'twitter.com' in url:
                return 'twitter'
            elif 'linkedin.com' in url:
                return 'linkedin'
            elif 'youtube.com' in url:
                return 'youtube'
            else:
                return 'unknown'


        socialUrls = []
        for url in socialLinks:
            socialUrls.append({'media': determine_media_type(url['href']), 'link': url['href']})

        social_media_map = {
            'facebook': '',
            'twitter': '',
            'instagram': '',
            'linkedin': '',
            'youtube': ''
        }

        for social_url in socialUrls:
            url = social_url['link']
            if 'facebook.com' in url:
                social_media_map['facebook'] = url
            elif 'twitter.com' in url:
                social_media_map['twitter'] = url
            elif 'instagram.com' in url:
                social_media_map['instagram'] = url
            elif 'linkedin.com' in url:
                social_media_map['linkedin'] = url
            elif 'youtube.com' in url:
                social_media_map['youtube'] = url



        entry = {
            "name": uniName.text.strip(),
            "location": {
                "country": "Germany",
                "state": stateName,
                "city": cityName.text.strip() if cityName else "N/A"
            },
            "logoSrc": logo['src'] if logo else "N/A",
            "type": type.text.strip() if type else "N/A",
            "establishedYear": foundedYear.text.strip() if foundedYear else "N/A",
            "contact": {
                "facebook": social_media_map['facebook'],
                "twitter": social_media_map['twitter'],
                "instagram": social_media_map['instagram'],
                "officialWebsite": uniLink['href'] if uniLink else "N/A",
                "linkedin": social_media_map['linkedin'],
                "youtube": social_media_map['youtube']
            }
        }
        universities.append(entry)

with open('universities.json', 'w', encoding='utf-8') as f:
    json.dump(universities, f, ensure_ascii=False, indent=4)

