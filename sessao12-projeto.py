### Atividade 12 ###

import requests
import re
import pandas as pd
from bs4 import BeautifulSoup 
import plotly.express as px
from urllib.parse import urljoin

### 11.1
base_url='http://books.toscrape.com'
url='https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
resposta = requests.get(url)
if resposta.status_code == 200:
    print('\nSucesso no download da pagina!')
else:
    print(f'Erro: {resposta.status_code}')

soup = BeautifulSoup(resposta.text, 'html.parser')

lista_livros = []

livros = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

for livro in livros:
    if livro.find('img', class_='thumbnail'):
    # Imagem
        img_alt = livro.find('img', class_='thumbnail').get('alt','vazio').strip()
        img = livro.find('img', class_='thumbnail').get('src','vazio').strip()
        full_url = urljoin(base_url, img)
        r = requests.get(full_url)
        nome_img = img.split('/')[-1]
        # Guardar a img no disco
        # with open(nome_img,'wb') as file:
        #     file.write(r.content)
        
    # Disponibilidade
        dispo = livro.find('p', class_='instock availability').get_text()
        if 'In stock' in dispo:
            in_stock = True
        elif 'Out of stock' in dispo:
            in_stock = False
        else:
            in_stock = None
        dispo = in_stock
    
    # Titulo
        book = livro.find('a', title=True)
        nome_livro = book.get('title')
        
    # Preco
        preco_livro = float(livro.find('p', class_='price_color').get_text().strip().split('€')[0].replace(',','.').encode('ascii', 'ignore'))
        
    # Classificação    
        classificacao = soup.find('p', class_='star-rating')
        rating = classificacao['class'][1]
        
    books = [nome_livro, preco_livro, dispo, rating]
    lista_livros.append(books)
    
df = pd.DataFrame(lista_livros, columns=['Título', 'Preço', 'Disponibilidade', 'Classificação'])
df.to_csv('livros.csv', index=False)