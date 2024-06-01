from flask import Flask, jsonify,redirect
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/scrape')

@app.route('/scrape')
def scrape():


    mp = []

    for i in range(1, 3):
        print(f"Scraping page {i}")
        url = f"https://www.flipkart.com/search?q=phone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}"
        try:
            response = requests.get(url)

            page_contents = response.text
            mp.append(page_contents)

        except Exception as err:
            print(f'Other error occurred for page {i}: {err}')

            continue



    phone_names = []
    phone_descriptions = []
    phone_prices = []
    phone_star_ratings = []
    product_links = []


    for data in mp:
        doc = BeautifulSoup(data, 'html.parser')

        name_of_phone_tags = doc.find_all('div', {'class': '_4rR01T'})
        phone_names.extend([tag.text.strip() for tag in name_of_phone_tags])

        phone_description_tags = doc.find_all('div', {'class': 'fMghEO'})
        phone_descriptions.extend([tag.text.strip() for tag in phone_description_tags])

        phone_price_tags = doc.find_all('div', {'class': '_30jeq3 _1_WHN1'})
        phone_prices.extend([tag.text.strip() for tag in phone_price_tags])

        phone_star_tags = doc.find_all('div', {'class': '_3LWZlK'})
        phone_star_ratings.extend([tag.text.strip() for tag in phone_star_tags])

        base_url = 'https://www.flipkart.com'
        product_links.extend([base_url + anchor_tag['href'] for anchor_tag in doc.find_all('a', class_='_1fQZEK')])

    max_len = max(len(phone_names), len(phone_descriptions), len(phone_prices), len(phone_star_ratings), len(product_links))
    phone_names += ['Null'] * (max_len - len(phone_names))
    phone_descriptions += ['Null'] * (max_len - len(phone_descriptions))
    phone_prices += ['Null'] * (max_len - len(phone_prices))
    phone_star_ratings += ['Null'] * (max_len - len(phone_star_ratings))
    product_links += ['Null'] * (max_len - len(product_links))

    phone_dict = {
        'name': phone_names,
        'description': phone_descriptions,
        'price': phone_prices,
        'star_rating': phone_star_ratings,
        'links': product_links
    }


    final_phone_data = pd.DataFrame(phone_dict)


    result = final_phone_data.to_json(orient='records')

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
