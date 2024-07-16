import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import re

# Año que deseas procesar
year = 2024

# Iterar sobre un rango del 1 al 30
for numero in range(30, 39):
    # Construir la URL dinámicamente usando f-string
    url = f'https://colombia.as.com/resultados/futbol/italia/2023_2024/jornada/regular_a_{numero}'

    # Realizamos una solicitud HTTP GET a la URL
    response = requests.get(url)

    # Verificamos que la solicitud fue exitosa
    if response.status_code == 200:
        # Parseamos el contenido HTML de la página con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraemos la información de los partidos
        partidos = []
        partidosConURL=[]
        for partido in soup.find_all('li', class_='list-resultado'):
            # Nombre del equipo local
            local = partido.find('div', class_='equipo-local').find('span', class_='nombre-equipo').text

            # Resultado del partido
            resultado_str = partido.find('div', class_='cont-resultado').find('a', class_='resultado').text.strip()
            partido_url = partido.find('div', class_='cont-resultado').find('a', class_='resultado')['href']
            goles_local, goles_visitante = resultado_str.split('-')

            # Convertir los goles a enteros
            goles_local = int(goles_local.strip())
            goles_visitante = int(goles_visitante.strip())

            # Nombre del equipo visitante
            visitante = partido.find('div', class_='equipo-visitante').find('span', class_='nombre-equipo').text

            # Fecha del partido
            fecha_str = partido.find('div', class_='info-evento').find('span', class_='fecha').text.strip()

            # Utilizamos expresiones regulares para identificar el formato correcto de fecha
            match = re.search(r'([A-Z])-(\d{2}/\d{2} \d{2}:\d{2})', fecha_str)
            if match:
                dia_semana = match.group(1)
                fecha_hora = match.group(2)
                fecha_str_con_año = f'{year} {fecha_hora}'

                try:

                        fecha = datetime.strptime(fecha_str_con_año, '%Y %d/%m %H:%M')





                except ValueError as e:
                    print(f'Error al convertir fecha {fecha_str_con_año}: {e}')
                    continue

            else:
                print(f'Formato de fecha no reconocido para {fecha_str}')
                continue

            # Agregamos la información del partido a la lista
            partidos.append((local, goles_local, goles_visitante, visitante, fecha))
            partidosConURL.append((local, goles_local, goles_visitante, visitante, fecha,partido_url))

            # Imprimir los datos del partido para verificar
            print(f'Partido: {local} {goles_local} - {goles_visitante} {visitante} {fecha}{partido_url}')


        # Conectamos a la base de datos MySQL
        conn = mysql.connector.connect(
            host='localhost',
            port=3310,
            user='root',
            password='',
            database='world_population_data'
        )
        cursor = conn.cursor()

        # Creamos la tabla si no existe
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS partidos (
            local VARCHAR(255),
            goles_local INT,
            goles_visitante INT,
            visitante VARCHAR(255),
            fecha DATETIME
        )
        ''')

        # Eliminar datos solo en la primera iteración
        if numero == 1:
            cursor.execute('DELETE FROM partidos')

        # Insertamos los datos en la tabla
        cursor.executemany(
            'INSERT INTO partidos (local, goles_local, goles_visitante, visitante, fecha) VALUES (%s, %s, %s, %s, %s)', partidos)

        # Confirmamos los cambios
        conn.commit()

        # Cerramos la conexión a la base de datos
        conn.close()

        print('Datos insertados exitosamente en la base de datos.')

        # Realizamos el scraping adicional para cada partido
        for partido in partidosConURL:
            partido_url = partido[5]
            response_partido = requests.get(partido_url)

            if response_partido.status_code == 200:
                soup_partido = BeautifulSoup(response_partido.content, 'html.parser')
                local_scorers = []
                visitante_scorers = []

                try:
                    # Extraer goleadores del equipo local
                    local_scorers_tag = soup_partido.find('div', class_='scr-hdr__team is-local').find('div',
                                                                                                       class_='scr-hdr__scorers')
                    if local_scorers_tag:
                        local_scorers = [scorer.text.strip() for scorer in local_scorers_tag.find_all('span')]
                except AttributeError:
                    print(f"No se encontraron goleadores locales en {partido_url}")

                try:
                    # Extraer goleadores del equipo visitante
                    visitante_scorers_tag = soup_partido.find('div', class_='scr-hdr__team is-visitor').find('div',
                                                                                                             class_='scr-hdr__scorers')
                    if visitante_scorers_tag:
                        visitante_scorers = [scorer.text.strip() for scorer in visitante_scorers_tag.find_all('span')]
                except AttributeError:
                    print(f"No se encontraron goleadores visitantes en {partido_url}")

                print(f'Local Scorers: {local_scorers}')
                print(f'Visitante Scorers: {visitante_scorers}')
            else:
                print(f'Error al realizar la solicitud para {partido_url}: {response_partido.status_code}')


else:
        print(f'Error al realizar la solicitud: {response.status_code}')

        """

           SELECT equipo, SUM(partidos_ganados) AS total_partidos_ganados
           FROM (
               SELECT local AS equipo, COUNT(*) AS partidos_ganados
               FROM partidos
               WHERE goles_local > goles_visitante
               GROUP BY local

               UNION ALL

               SELECT visitante AS equipo, COUNT(*) AS partidos_ganados
               FROM partidos
               WHERE goles_visitante > goles_local
               GROUP BY visitante
           ) AS partidos_ganados_total
           GROUP BY equipo


           """





