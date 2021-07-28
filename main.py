import requests
from bs4 import BeautifulSoup


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
base_list = []
file = open('base.txt', 'w')

def information_parser(link_list:list):
    for product in link_list:
        response = requests.get(product, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        print('Name —{}'.format(soup.find('h1', class_='product__title').get_text()))
        base_list.append(
            [
                'Name —{}'.format(soup.find('h1', class_='product__title').get_text()), " "
                'Cod product — {}'.format(int((soup.find('p', class_='product__code detail-code').get_text()[-10:].replace(' ', '')))), " "
                'Link product — {}'.format(product), " "
                'Link photo — {}'.format(soup.find('img', class_='picture-container__picture').get('src')), " "
                'Features — {}'.format(soup.find('p', class_='product-about__brief ng-star-inserted').get_text())
            ]
        )
    return base_list


def generator_pages():
    page = 1
    while True:
        if page == 1:
            response = requests.get("https://rozetka.com.ua/notebooks/c80004/", headers=HEADERS)
        else:
            response = requests.get("https://rozetka.com.ua/notebooks/c80004/page={}/".format(page), headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.find_all("li", "catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted")
        if len(items):
            product = []
            for item in items:
                product.append(
                        item.find('div', class_="goods-tile__inner").find("a").get("href")
                )
            information_parser(product)
            page += 1
            print('{0}\nСтраница обработана {1}\n{0}'.format("-" * 21,page - 1))
            for temp_list in base_list:
                print("".join([out_list for out_list in temp_list]))
                file.write("".join([out_list for out_list in temp_list]))
                file.write("\n")
        else:
            break

generator_pages()



