import requests
import smtplib
from http.cookiejar import MozillaCookieJar
from bs4 import BeautifulSoup


def send_email():
    my_email = '87vmehta.test@gmail.com'
    password = 'uznaelgyfuhxpgwz'
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        try:
            product_title = soup.find('span', id="productTitle")
            connection.sendmail(
                from_addr=my_email,
                to_addrs='87vmehta.test@gmail.com',
                msg=f"Subject:Your Amazon Product hit its Strike Price!!\n\n"
                    f"\n{product_title.getText()}\n"
                    f"\nYour strike price was: ${strike_price:.2f}\n"
                    f"\nIt's now at: ${price:.2f}\n"
                    f"\nHere's the link:\n{url_input}"
            )
        except UnicodeEncodeError:
            product_title = soup.find('span', class_="a-size-base a-color-tertiary")
            connection.sendmail(
                from_addr=my_email,
                to_addrs='87vmehta.test@gmail.com',
                msg=f"Subject:Your Amazon Product hit its Strike Price!!\n"
                    f"\n{product_title.getText()}\n"
                    f"\nYour strike price was: ${strike_price:.2f}\n"
                    f"\nIt's now at: ${price:.2f}\n"
                    f"\nHere's the link:\n{url_input}"
            )


url_input = input('Copy and paste the Amazon.ca url here: ')
strike_price = float(input('What is your minimum price?? :$'))

cookie_file = 'amazon.ca_cookies.txt'
jar = MozillaCookieJar(cookie_file)
s = requests.Session()
s.cookies = jar
s.cookies.load()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
}

response = s.get(url=url_input, headers=headers)
website = response.text
soup = BeautifulSoup(website, 'html.parser')
dollars = soup.find('span', class_='a-price-whole')
cents = soup.find('span', class_='a-price-fraction')
price = float(dollars.getText() + cents.getText())


# print(price)
# print(type(price))
if price <= strike_price:
    send_email()
    print('sent you an email!')
