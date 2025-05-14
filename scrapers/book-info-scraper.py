import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://books.toscrape.com/catalogue/"
start_url = urljoin(base_url, "page-1.html")

current_url = start_url

with open('book-data.txt', 'w', encoding='utf-8') as file:
    while True:
        # base_url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        r = requests.get(current_url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
        for item in items:
            title = item.find('h3').find('a')['title']
            price = item.find('p', class_='price_color').text.strip()
            availability = item.find('p', class_='instock availability')
            rating = item.find('p', class_='star-rating')
            link = urljoin(base_url, item.find('a')['href'])
            file.write("Name: " + title + '\n')
            file.write("Price: " + price + '\n')
            file.write("Availability: " + availability.text.strip() + '\n')
            file.write("Rating: " + rating['class'][1] + '\n')
            file.write(f"Link: {link}\n\n")
            # full_url = urljoin(home_url, a_tag['href'])
            # file.write("Link: " + full_url + '\n\n')
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page = next_button.find('a')['href']
            current_url = urljoin(current_url, next_page)
        else:
            break
        
        # titles = soup.find_all('h3')
        # for title in titles:
        #     file.write(title.text + '\n')
        # prices = soup.find_all('p', class_='price_color')
        # for price in prices:
        #     file.write(price.text + '\n')
        
        # articles = soup.find_all('article')
        # links = set()
        # for article in articles:
        #     a_tags = article.find_all('a')
        #     for a_tag in a_tags:
        #         if 'href' in a_tag.attrs:
        #             full_url = urljoin(home_url, a_tag['href'])
        #             links.add(full_url)
        # for link in links:
        #     file.write(link + '\n')

# url = "https://books.toscrape.com/catalogue/page-1.html"
# r = requests.get(url).text
# soup = BeautifulSoup(r, 'html.parser')
# articles = soup.find_all('article')
# herfs = set()
# with open('book-data.txt', 'w', encoding='utf-8') as file:
#     for article in articles:
#         links_in_article = article.find_all('a')
#         for a in links_in_article:
#             herfs.add(a['href'])
#             file.write(str(a['href']) + '\n')


# with open('book-data.txt') as file:
#     soup = BeautifulSoup(file, 'html.parser')
#     html = soup.prettify()
#     print(soup.find_all('article'))