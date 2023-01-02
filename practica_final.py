from bs4 import BeautifulSoup
import pandas as pd
import requests
import fpdf

# Se incluyen estas 2 líneas para que no de error la librería matplotlib
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt


def extraerDatosEquipo():
    # Extraemos los datos de la API
    url = "https://api-basketball.p.rapidapi.com/statistics"

    querystring = {"season":"2022-2023","league":"12","team":"133"}

    headers = { 
        "X-RapidAPI-Key": "INSERTAR CLAVE",
        "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    return response

def extraerDatosPronostico():
    # Extraemos los datos mediante WebScraping
    url = "https://www.sportytrader.es/pronosticos/baloncesto/usa/nba-306/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pronosticos = soup.find_all('div', class_="w-full xl:w-2/5 flex justify-center items-center py-4")

    # Escogemos solo el pronosticos que sea de los Boston Celtics
    pronostico_celtics = ""
    for pronostico in pronosticos:
        nombres = pronostico.find_all('div', class_="w-1/2 text-center break-word p-1 dark:text-white")
        for nombre in nombres:
            if "Boston Celtics" in nombre.text:
                pronostico_celtics = pronostico

    return pronostico_celtics


def transformarDatosEquipo(response):
    datos = response.json()["response"]
    games = datos["games"]
    games['wins']['home'] = games['wins']['home']['total']
    games['wins']['away'] = games['wins']['away']['total']
    games['wins']['all'] = games['wins']['all']['total']
    games['loses']['home'] = games['loses']['home']['total']
    games['loses']['away'] = games['loses']['away']['total']
    games['loses']['all'] = games['loses']['all']['total']
    games['draws']['home'] = games['draws']['home']['total']
    games['draws']['away'] = games['draws']['away']['total']
    games['draws']['all'] = games['draws']['all']['total']

    points_raw = datos["points"]
    points_raw['for'] = points_raw['for']['total']
    points_raw['against'] = points_raw['against']['total']
    points = {}
    points['points_for'] = points_raw['for']
    points['points_against'] = points_raw['against']


    df_games = pd.DataFrame(games)
    df_points = pd.DataFrame(points)

    df = pd.concat([df_games, df_points], axis=1)

    return df

def transformarDatosPronostico(pronostico_celtics):
    # Transformamos los datos del pronostico para que sean legibles

    if pronostico_celtics != "":
        equipo1 = ["", -1] # [Nombre del equipo, 1=Ganador | 0=Perdedor]
        equipo2 = ["", -1]
        equipos = pronostico_celtics.find_all('div', class_="w-1/2 text-center break-word p-1 dark:text-white")
        equipo1[0] = equipos[0].text.replace("\n", "")
        equipo2[0] = equipos[1].text.replace("\n", "")

        prediccion = pronostico_celtics.find('div', class_="flex w-24 justify-around items-center")
        prediccion = prediccion.find_all('span')
        if prediccion[0]['class'][6] == 'bg-gray-200':
            equipo1[1] = 0
            equipo2[1] = 1
        elif prediccion[0]['class'][7] == 'bg-primary-green':
            equipo1[1] = 1
            equipo2[1] = 0

        pronostico = [equipo1, equipo2]
        return pronostico
    else:
        return []


def cargarPDF(df, pronostico):
    # Creamos gráficas con los datos del equipo
    # y las guardamos en un reporte PDF

    # Gráfica de los partidos jugados en casa
    plt.figure(figsize=(10, 5))
    plt.bar(df.columns[1:4], df.iloc[0, 1:4], color='green')
    plt.title('Partidos jugados en casa')
    plt.savefig('partidos_casa.png')

    # Gráfica de los partidos jugados fuera de casa
    plt.figure(figsize=(10, 5))
    plt.bar(df.columns[1:4], df.iloc[1, 1:4], color='red')
    plt.title('Partidos jugados fuera de casa')
    plt.savefig('partidos_fuera.png')

    # Gráfica de los partidos jugados en total
    plt.figure(figsize=(10, 5))
    plt.bar(df.columns[1:4], df.iloc[2, 1:4], color='blue')
    plt.title('Partidos jugados en total')
    plt.savefig('partidos_total.png')

    # Gráfica de los puntos a favor y en contra en casa
    plt.figure(figsize=(10, 5))
    plt.bar(df.columns[4:6], df.iloc[0, 4:6], color='orange')
    plt.title('Puntos a favor y en contra en casa')
    plt.savefig('puntos_casa.png')

    # Gráfica de los puntos a favor y en contra fuera de casa
    plt.figure(figsize=(10, 5))
    plt.bar(df.columns[4:6], df.iloc[1, 4:6], color='purple')
    plt.title('Puntos a favor y en contra fuera de casa')
    plt.savefig('puntos_fuera.png')

    # Gráfica de los puntos a favor y en contra en total
    plt.figure(figsize=(10, 5))
    plt.bar(df.columns[4:6], df.iloc[2, 4:6], color='brown')
    plt.title('Puntos a favor y en contra en total')
    plt.savefig('puntos_total.png')

    # Creamos el reporte PDF
    pdf = fpdf.FPDF()

    pdf.add_page()
    pdf.image('logo.jpg', x=8, y=8, w=24)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(190, 10, 'Reporte de estadísticas del equipo Boston Celtics', align='C')
    pdf.ln(20)
    pdf.set_font('Arial', '', 12)
    pdf.cell(190, 10, 'Estadisticas de victorias y derrotas', align='C')
    pdf.image('partidos_casa.png', x=10, y=40, w=180)
    pdf.image('partidos_fuera.png', x=10, y=125, w=180)
    pdf.image('partidos_total.png', x=10, y=210, w=180)

    pdf.add_page()
    pdf.image('logo.jpg', x=8, y=8, w=24)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(190, 10, 'Reporte de estadísticas del equipo Boston Celtics', align='C')
    pdf.ln(20)
    pdf.set_font('Arial', '', 12)
    pdf.cell(190, 10, 'Estadisticas de puntos del equipo', align='C')
    pdf.image('puntos_casa.png', x=30, y=40, w=140)
    pdf.image('puntos_fuera.png', x=30, y=110, w=140)
    pdf.image('puntos_total.png', x=30, y=180, w=140)

    pdf.ln(220)
    pdf.cell(190, 5, 'Pronostico del proximo partido', align='C')
    if pronostico != []:
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)
        pdf.cell(190, 10, 'Partido: ' + pronostico[0][0] + ' vs ' + pronostico[1][0], align='C')
        pdf.ln(10)
        pdf.cell(190, 5, 'Pronóstico: ' + pronostico[0][0] + ' gana' if pronostico[0][1] == 1 else pronostico[1][0] + ' gana', align='C')
    else:
        pdf.ln(10)
        pdf.cell(190, 5, 'No hay pronóstico para el proximo partido de los Boston Celtics', align='C')
        pdf.ln(10)
        pdf.cell(190, 5, 'Se buscó el pronóstico en: https://www.sportytrader.es/pronosticos/baloncesto/usa/nba-306/', align='C')

    pdf.output('reporte.pdf', 'F')

    return


def main():
    # Extraemos los datos
    response = extraerDatosEquipo()
    pronostico_celtics = extraerDatosPronostico()

    # Transformamos los datos
    df = transformarDatosEquipo(response)
    pronostico = transformarDatosPronostico(pronostico_celtics)

    cargarPDF(df, pronostico)

    print('\nReporte generado con éxito')
    print("\nPronóstico del próximo partido de los Boston Celtics:")
    if pronostico != []:
        print('\tPartido: ' + pronostico[0][0] + ' vs ' + pronostico[1][0])
        print('\tPronóstico: ' + pronostico[0][0] + ' gana\n' if pronostico[0][1] == 1 else '\tPronóstico: ' + pronostico[1][0] + ' gana\n')
    else:
        print('\tNo hay pronóstico para el proximo partido de los Boston Celtics')
        print('\tSe buscó el pronóstico en: https://www.sportytrader.es/pronosticos/baloncesto/usa/nba-306/\n')

    return

if __name__ == "__main__":
    main()