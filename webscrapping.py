#importar las librerias

#Utilizada para hacer solicitudes HTTP a páginas web.
import requests
#Permite el parsing y manipulación de documentos HTML
from bs4 import BeautifulSoup
# Proporciona la interfaz para conectarse
# y ejecutar consultas a una base de datos MySQL.
import mysql.connector


#Índices de columnas en la tabla HTML donde se encuentran los datos que necesitas procesar.
YEARLY_CHANGE = 3
URBAN_POP = 10
WORLD_SHARE = 11

#Número máximo de intentos para reintentar la solicitud HTTP en caso de error.

MAX_RETRIES = 3

""" --------   clean_percentage    ----------
Función para limpiar y convertir porcentajes a números decimales,
eliminando el símbolo '%' y convirtiéndolo a float.
"""
def clean_percentage(percentage):
    if percentage.endswith('%'):
        return float(percentage.replace('%', '').strip()) / 100
    return None

def process_row(celdas):
    row_data = []
    for i, td in enumerate(celdas):
        text = td.get_text(strip=True)
        if i in (YEARLY_CHANGE, URBAN_POP, WORLD_SHARE):

            if text == "N.A." or text == "":
                text = None
            else:
                text = clean_percentage(text)
        elif i != 1:
            if text == "N.A." or text == "":
                text = None
            else:
                text = text.replace(',', '').strip()
                try:
                    text = float(text)
                except ValueError:
                    pass
        row_data.append(text)
    return row_data

"""Función principal que realiza la solicitud HTTP a la url, parsea la respuesta
 usando BeautifulSoup para encontrar una tabla HTML. Luego itera sobre las fila
 s de la tabla, procesa cada fila usando process_row y ejecuta una consulta de 
 inserción SQL en la base de datos MySQL."""

def process_url(url, cursor, sql_insert, db):

    ### max_retries defin el numero de iteraciones por si ocurre algun error
    for _ in range(MAX_RETRIES):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f'Error al acceder a {url}: Código de estado {response.status_code}')
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            tabla = soup.find('table')
            if tabla:
                for fila in tabla.find_all('tr')[1:]:  # Omitir el encabezado
                    celdas = fila.find_all('td')
                    if celdas and len(celdas) == 12:
                        row_data = process_row(celdas)
                        if len(row_data) == 12:
                            cursor.execute(sql_insert, row_data)
                        else:
                            print("Número incorrecto de elementos en row_data:", row_data)
                db.commit()
                print(f'Datos de la tabla exportados correctamente a la base de datos MySQL')
            else:
                print("No se encontró tabla válida en la página.")
            break
        except requests.RequestException as e:
            print(f'Error de solicitud para {url}: {str(e)}')
        except Exception as e:
            print(f'Error al procesar datos de {url}: {str(e)}')

def main():
    # db_config configura la conexion a bae de datos
    db_config = {
        "host": "localhost",
        "port": 3310,
        "user": "root",
        "password": "",
        "database": "world_population_data"
    }

    sql_create_table = """
       CREATE TABLE IF NOT EXISTS population_2 (
           ranq VARCHAR(255),
           country VARCHAR(255),
           population VARCHAR(255),
           yearlychange VARCHAR(255),
           netchange VARCHAR(255),
           density VARCHAR(255),
           landarea VARCHAR(255),
           migrants VARCHAR(255),
           fertrate VARCHAR(255),
           medaage VARCHAR(255),
           urbanpop VARCHAR(255),
           worldshare VARCHAR(255)
       )
       """

    sql_insert = """
    INSERT INTO population (ranq, country, population, yearlychange, netchange, density, landarea, migrants, fertrate, medaage, urbanpop, worldshare)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    urls = ['https://www.worldometers.info/world-population/population-by-country/']
    try:


        #se conecta a la base de datos
        # los dos ** desempaqueta el diccionario y pasa los parametros db_config
        db = mysql.connector.connect(**db_config)

        """2ara crear un objeto cursor. Este objeto 
         cursor permite ejecutar comandos SQL en la base de datos conectada"""


        cursor = db.cursor()
        for url in urls:
            process_url(url, cursor, sql_insert, db)
    except mysql.connector.Error as e:
        print(f'Error de MySQL: {str(e)}')
    finally:
        cursor.close()

        db.close()

if __name__ == "__main__":
    main()
