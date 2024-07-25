import requests
from bs4 import BeautifulSoup

# URL de búsqueda en Google (ejemplo para "Juegos Olímpicos")
query = "Juegos Olímpicos"
url = f"https://www.google.com/search?q={query}"

# Realizamos una solicitud HTTP GET a la URL
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

# Verificamos que la solicitud fue exitosa
if response.status_code == 200:
    # Parseamos el contenido HTML de la página con BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraemos la información de los resultados de búsqueda
    resultados = []

    # Actualizamos los selectores de acuerdo con la estructura actual
    for resultado in soup.find_all('a', class_='BVG0Nb pijXPc'):
        # Título y Enlace
        titulo_div = resultado.find('div', class_='BNeawe')
        titulo = titulo_div.find('span', class_='rQMQod Xb5VRe').get_text() if titulo_div else 'No title'
        enlace = resultado['href'] if 'href' in resultado.attrs else 'No link'

        # Descripción
        descripcion_div = resultado.find('div', class_='BNeawe tAd8D AP7Wnd')
        descripcion = descripcion_div.get_text() if descripcion_div else 'No description'

        # Construir el enlace completo
        if enlace.startswith('/url?q='):
            enlace = enlace.split('/url?q=')[1].split('&')[0]

        resultados.append({
            'titulo': titulo,
            'enlace': enlace,
            'descripcion': descripcion
        })

    # Imprimimos los resultados
    for resultado in resultados:
        print(f"Título: {resultado['titulo']}")
        print(f"Enlace: {resultado['enlace']}")
        print(f"Descripción: {resultado['descripcion']}")
        print("-" * 40)
else:
    print("Error al realizar la solicitud")
