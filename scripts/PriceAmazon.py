import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def findPriceFromAmazon(time):

    # URL del producto
    url = 'https://www.amazon.com.mx/ASUS-Graphics-Retroiluminado-Garant%C3%ADa-Servicio/dp/B0DGJRW392/ref=pd_ci_mcx_pspc_dp_2_t_1?pd_rd_w=l6HZn&content-id=amzn1.sym.01e1a2c3-d502-464a-90a5-f932c8c4ef07&pf_rd_p=01e1a2c3-d502-464a-90a5-f932c8c4ef07&pf_rd_r=YMYYJ56XGP1G581DJFB8&pd_rd_wg=r3ny1&pd_rd_r=b6c7f928-94d6-49a7-8205-1b4ca0421f9c&pd_rd_i=B0DGJRW392'

    # Realiza la petición a la URL y controla posibles excepciones
    try:
        response = requests.get(url)
        response.raise_for_status()  # Genera una excepción si el estado no es 200
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        exit()

    try:
        # Procesa el contenido de la respuesta con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Obtiene el precio del producto
        price_element = soup.find('span', class_='a-offscreen')
        if price_element:
            price = price_element.get_text().strip()
        else:
            price = "Precio no disponible"
        
        # Obtiene la tabla de descripción del producto
        descriptionTable = soup.find('table', class_='a-normal a-spacing-micro')
        if not descriptionTable:
            raise ValueError("No se encontró la tabla de descripciones.")

        # Extrae los nombres de las columnas y sus descripciones
        collunName = [description.text.strip() for description in descriptionTable.find_all('td', class_='a-span3')]
        descriptions = [description.text.strip() for description in descriptionTable.find_all('td', class_='a-span9')]

        # Limpia los datos y verifica integridad
        if len(collunName) != len(descriptions):
            raise ValueError("El número de columnas no coincide con el número de descripciones.")

        # Combina los datos en un diccionario
        data = {collunName[i]: descriptions[i] for i in range(len(collunName))}
        data = {"Precio": price, **data}
        data ={"Fecha_Busqueda": time, **data}
        # Crea un DataFrame con los datos
        df = pd.DataFrame([data])

        # Crea el directorio 'data' si no existe
        os.makedirs('data', exist_ok=True)

        # Ruta del archivo CSV
        output_file = 'data/prices.csv'

        # Verifica si el archivo ya existe
        if os.path.isfile(output_file):
            # Si el archivo existe, agrega los datos sin sobrescribir el encabezado
            df.to_csv(output_file, mode='a', header=False, index=False)
        else:
            # Si el archivo no existe, lo crea con encabezados
            df.to_csv(output_file, mode='w', header=True, index=False)

        print("Datos guardados exitosamente en:", output_file)

    except Exception as e:
        print(f"Error al procesar los datos: {e}")
