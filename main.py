import requests
from bs4 import BeautifulSoup
import lxml
import os
from smtplib import SMTP

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

URL = "https://www.amazon.com/AMD-Ryzen-3700X-16-Thread-Processor/dp/B07SXMZLPK/" \
      "ref=sr_1_3?dchild=1&qid=1620563679&s=computers-intl-ship&sr=1-3"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}
response = requests.get(URL, headers=headers)
product_web_page = response.text

soup = BeautifulSoup(product_web_page, 'lxml')

price = float(soup.find(name="span", id="priceblock_ourprice").getText().replace("$", ""))
title = soup.find(name="span", id="productTitle").getText()

if price <= 250:
    with SMTP(host="smtp.gmail.com") as smtp:
        smtp.starttls()
        smtp.login(user=EMAIL,
                   password=PASSWORD)
        smtp.sendmail(EMAIL,
                      EMAIL,
                      f"Subject:Amazon Price Alert!\n\n"
                      f"{title.strip()}\n"
                      f"Now: ${price}\n"
                      f"{URL}")