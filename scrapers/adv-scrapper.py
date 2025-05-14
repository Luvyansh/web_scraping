import requests
from bs4 import BeautifulSoup as bs
import csv
from urllib.parse import urljoin

with open("quotes-to-scrape.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['No.', 'Text', 'Author', 'Born Date and Location'])
    
    LOGIN_URL = "https://quotes.toscrape.com/login"
    QUOTES_URL = "https://quotes.toscrape.com/page/{}/"
    base_url = "https://quotes.toscrape.com"
    
    session = requests.Session()
    headers = {
        "User-Agent": "Chrome/111.0.0.0"
    }
    login_page = session.get(LOGIN_URL, headers=headers)
    soup = bs(login_page.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"}).get("value")
    payload = {
        "csrf_token": csrf_token,
        "username": "admin",
        "password": "admin"
    }
    res = session.post(LOGIN_URL, data=payload, headers=headers)
    if "Logout" not in res.text:
        print("Login Failed!")
        exit()
    else:
        print("Logged in!!!")
    page_num = 1
    quote_num = 1
    while True:
        response = session.get(QUOTES_URL.format(page_num), headers=headers)
        response.encoding = 'utf-8'
        soup = bs(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")
        if not quotes:
            break
        for quote in quotes:
            author_details = quote.find("a", href=True)
            r = session.get(base_url + author_details["href"], headers=headers)
            s = bs(r.text, "html.parser")
            date = s.find("span", class_="author-born-date").text.strip()
            loc = s.find("span", class_="author-born-location").text.strip()
            writer.writerow([
                quote_num,
                quote.find("span", class_="text").text,
                quote.find("small", class_="author").text,
                f"{date} {loc}"
            ])
            quote_num += 1
        next_page = soup.find("li", class_="next")
        if not next_page:
            break
        page_num += 1