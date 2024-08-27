import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en,mr;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

max_restaurants = 500

review_limit = 250

def scrape_restaurant_links(page_url):
    time.sleep(2)

    response = requests.get(page_url, headers=headers, timeout=5, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

    restaurant_links = []
    restaurant_names = []

    restaurant_list = soup.find_all('div', class_='biGQs _P fiohW alXOW NwcxK GzNcM ytVPx UTQMg RnEEZ ngXxk')

    if not restaurant_list:
        return [], []

    for restaurant in restaurant_list:
        restaurant_name_tag = restaurant.find('a', class_='BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS')
        name = restaurant_name_tag.get_text(strip=True)
        link = 'https://www.tripadvisor.com.br' + restaurant_name_tag.get('href')
        restaurant_names.append(name)
        restaurant_links.append(link)

    return restaurant_names, restaurant_links

def scrape_restaurant_reviews(restaurant_url):
    restaurant_reviews = []

    while restaurant_url and len(restaurant_reviews) < review_limit:
        time.sleep(2)
        response = requests.get(restaurant_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        restaurant_review_bodies = soup.find_all('div', attrs={'data-test-target': 'review-body'})

        for restaurant_review_body in restaurant_review_bodies:
            restaurant_review = restaurant_review_body.find('span', class_='JguWG')
            if restaurant_review:
                review_text = restaurant_review.get_text(strip=True)
                restaurant_reviews.append(review_text)
                if len(restaurant_reviews) >= review_limit:
                    break

        if len(restaurant_reviews) >= review_limit:
            break

        next_page = soup.find('a', attrs={'aria-label': 'Próxima página'})

        if next_page and 'href' in next_page.attrs:
            restaurant_url = 'https://www.tripadvisor.com.br' + next_page['href']
        else:
            restaurant_url = None

    return ' '.join(restaurant_reviews)

def scrape_trip_advisor_restaurants(start_url):
    all_restaurants = []

    print("QTD RESTAURANTES: ", len(all_restaurants))

    current_url = start_url

    while current_url and len(all_restaurants) < max_restaurants:
        print(f'Scraping page: {current_url}...')
        time.sleep(2)

        names, links = scrape_restaurant_links(current_url)

        for name, link in zip(names, links):
            print(f'Scraping restaurant: {name} - {link}')
            description = scrape_restaurant_reviews(link)

            if description:
                all_restaurants.append({
                    'Name': name,
                    'Description': description
                })

            if len(all_restaurants) >= max_restaurants:
                break

        response = requests.get(current_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        next_page = soup.find('a', attrs={'aria-label': 'Próxima página'})

        if next_page and 'href' in next_page.attrs:
            current_url = 'https://www.tripadvisor.com.br' + next_page['href']
        else:
            current_url = None

    return pd.DataFrame(all_restaurants)

start_url = 'https://www.tripadvisor.com.br/Restaurants-g303631-Sao_Paulo_State_of_Sao_Paulo.html'

df = scrape_trip_advisor_restaurants(start_url)

df.to_csv('trip_advisor_restaurants_sp.csv', index=False)
print(f'Scraping concluído. {len(df)} restaurantes salvos no arquivo trip_advisor_restaurants_sp.csv')