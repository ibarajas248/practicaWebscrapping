import requests
from bs4 import BeautifulSoup

# URL de la página web a la que vamos a hacer scraping
url = "https://colombia.as.com/resultados/futbol/italia/2023_2024/directo/regular_a_1_444160/"

# Hacer una solicitud GET a la URL
response = requests.get(url)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    # Analizar el contenido HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos los divs con la clase 'team team-b'
    teams = soup.find_all('div', class_='team team-b')

    for team in teams:
        # Extraer el nombre del equipo
        team_name = team.find('span', class_='large').text
        # Extraer el abreviatura del equipo
        team_abbr = team.find('abbr', class_='short').text
        # Extraer el logo del equipo
        team_logo = team.find('img', class_='team-logo')['src']
        # Extraer el puntaje del equipo
        team_score = team.find('span', class_='team-score').text
        # Extraer el div de anotadores
        scorers_div = team.find('div', class_='scorers')

        # Extraer los anotadores si existen
        if scorers_div:
            # Iterar sobre los <span> dentro del div de anotadores
            visitante_scorers = [scorer.text.strip() for scorer in scorers_div.find_all('span')]
        else:
            visitante_scorers = []

        print(f"Equipo: {team_name} ({team_abbr})")
        print(f"Logo: {team_logo}")
        print(f"Puntaje: {team_score}")
        print(f"Anotadores: {', '.join(visitante_scorers)}")
        print("-" * 40)

else:
    print(f"Error al acceder a la página: {response.status_code}")
