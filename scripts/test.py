import requests
from bs4 import BeautifulSoup
import pandas as pd

print ("Web Scraping test 1")
#url objetivo
url = 'https://www.iuv.edu.mx/oferta-academica/maestrias/ciencia-datos-inteligencia-negocios/'
#Relaliza la solicitud http
response  = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    #extrae títulos
    titles =[title.text for title in soup.find_all('h5')]
    #Guarda daton en un DataFrame
    df = pd.DataFrame({'Titles': titles})
    df.to_csv('data/titles.csv', index=False)
    print("Datos guardados en 'data/titles.csv")
else:
    print(f"Error:{response.status_code}")
