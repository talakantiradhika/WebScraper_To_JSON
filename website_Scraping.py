import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.4icu.org/de/universities/"
def extract_university_info(university_element):
    try:
        name = university_element.find('a', class_='university-name').text.strip()
        logo_url = university_element.find('img')['src']
        details = university_element.find('div', class_='university-details').text.strip().split('\n')
        type_ = details[0].split(':')[1].strip()
        founded_year = details[1].split(':')[1].strip()
        location = details[2].split(':')[1].strip().split(', ')
        phone_number = details[3].split(':')[1].strip()

        social_media_urls = {
            "facebook": university_element.find('a', class_='facebook')['href'] if university_element.find('a', class_='facebook') else '',
            "twitter": university_element.find('a', class_='twitter')['href'] if university_element.find('a', class_='twitter') else '',
            "instagram": university_element.find('a', class_='instagram')['href'] if university_element.find('a', class_='instagram') else '',
            "officialWebsite": university_element.find('a', class_='website')['href'] if university_element.find('a', class_='website') else '',
            "linkedin": university_element.find('a', class_='linkedin')['href'] if university_element.find('a', class_='linkedin') else '',
            "youtube": university_element.find('a', class_='youtube')['href'] if university_element.find('a', class_='youtube') else ''
        }
        return {
            "name": name,
            "location": {
                "country": "Germany",
                "state": location[0],
                "city": location[1] if len(location) > 1 else ''
            },
            "logoSrc": logo_url,
            "type": type_,
            "establishedYear": founded_year,
            "contact": social_media_urls
        }
    except Exception as e:
        print(f"Error extracting university info: {e}")
        return None

def main():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    universities_data = []
    university_elements = soup.find_all('div', class_='university-item')
    for university_element in university_elements:
        university_info = extract_university_info(university_element)
        if university_info:
            universities_data.append(university_info)
    with open('universities_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(universities_data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
