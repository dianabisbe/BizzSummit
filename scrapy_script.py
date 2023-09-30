# pylint: skip-file

# Paso 1a: Instalar Selenium y Scrapy
# Selenium es una biblioteca popular para la automatización web.
# Scrapy es una herramienta ampliamente utilizada para el web scraping.
# Puedes instalar estas bibliotecas con pip.

# pip install selenium
# pip install scrapy

# Paso 1b: Descargar chromedriver
# Selenium requiere el controlador de Chrome para interactuar con el navegador.
# Descarga el chromedriver correspondiente a tu versión de Chrome desde el sitio oficial de Chrome.
# Coloca el archivo chromedriver.exe en la misma carpeta donde se ejecutará tu código.

# Paso 2: Importar bibliotecas
# Importa las bibliotecas necesarias para realizar el web scraping y procesar los datos.

import numpy as np
import pandas as pd
from scrapy.selector import Selector
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

# Paso 3: Selenium Test
# Abre una instancia del navegador Chrome y visita la URL de las reseñas de IMDb.
# Luego, realiza un desplazamiento hacia abajo en la página para cargar más reseñas.

driver = webdriver.Chrome('chromedriver.exe')
url = 'https://www.imdb.com/title/tt0241527/reviews?ref_=tt_sa_3'
time.sleep(1)
driver.get(url)
time.sleep(1)
print(driver.title)
time.sleep(1)
body = driver.find_element(By.CSS_SELECTOR, 'body')
body.send_keys(Keys.PAGE_DOWN)
time.sleep(1)
body.send_keys(Keys.PAGE_DOWN)
time.sleep(1)
body.send_keys(Keys.PAGE_DOWN)

# Paso 4: Extraer la cantidad de reseñas
# Utilizamos Scrapy Selector para extraer la cantidad total de reseñas desde la página.

sel = Selector(text=driver.page_source)
review_counts = sel.css('.lister .header span::text').extract_first().replace(',', '').split(' ')[0]
more_review_pages = int(int(review_counts) / 25)

# Paso 5: Cargar todas las reseñas
# Dado que cada página muestra solo 25 reseñas, hacemos clic en el botón "Load all reviews" para cargar todas las reseñas.
# Iteramos sobre el número de páginas adicionales a cargar.

for i in tqdm(range(more_review_pages)):
    try:
        css_selector = 'load-more-trigger'
        driver.find_element(By.ID, css_selector).click()
    except:
        pass

# Paso 6: Extraer reseñas de HTML (ejemplo para la primera reseña)
# Utilizamos Scrapy Selector para extraer información específica de cada reseña, como calificación, texto, fecha, autor, título y URL.

reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')
first_review = reviews[0]
sel2 = Selector(text=first_review.get_attribute('innerHTML'))
rating = sel2.css('.rating-other-user-rating span::text').extract_first().strip()
review = sel2.css('.text.show-more__control::text').extract_first().strip()
review_date = sel2.css('.review-date::text').extract_first().strip()
author = sel2.css('.display-name-link a::text').extract_first().strip()
review_title = sel2.css('a.title::text').extract_first().strip()
review_url = sel2.css('a.title::attr(href)').extract_first().strip()
helpfulness = sel2.css('.actions.text-muted::text').extract_first().strip()

# Paso 7: Combinar toda la información
# Iteramos sobre todas las reseñas para extraer y almacenar la información en listas.

rating_list = []
review_date_list = []
review_title_list = []
author_list = []
review_list = []
review_url_list = []
error_url_list = []
error_msg_list = []

for d in tqdm(reviews):
    try:
        sel2 = Selector(text=d.get_attribute('innerHTML'))
        rating = sel2.css('.rating-other-user-rating span::text').extract_first()
        review = sel2.css('.text.show-more__control::text').extract_first()
        review_date = sel2.css('.review-date::text').extract_first()
        author = sel2.css('.display-name-link a::text').extract_first()
        review_title = sel2.css('a.title::text').extract_first()
        review_url = sel2.css('a.title::attr(href)').extract_first()
        
        rating_list.append(rating)
        review_date_list.append(review_date)
        review_title_list.append(review_title)
        author_list.append(author)
        review_list.append(review)
        review_url_list.append(review_url)
    except Exception as e:
        error_url_list.append(url)
        error_msg_list.append(e)

# Paso 8: Crear un DataFrame con los datos extraídos
# Utilizamos Pandas para crear un DataFrame con los datos extraídos de las reseñas.

review_df = pd.DataFrame({
    'Review_Date': review_date_list,
    'Author': author_list,
    'Rating': rating_list,
    'Review_Title': review_title_list,
    'Review': review_list,
    'Review_Url': review_url_list
})

# Paso 9: Imprimir el DataFrame o guardar los datos
# Puedes imprimir el DataFrame o guardar los datos en un archivo CSV para su posterior análisis en Power BI y Azure AI.

print(review_df)
