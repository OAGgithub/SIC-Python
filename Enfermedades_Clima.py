import requests
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns

def obtener_temperatura(localidad, api_key):
    parameters = {'key': api
                  _key, 'place_id': localidad}
    url = "https://www.meteosource.com/api/v1/free/point"

    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        data = response.json()

        if 'current' in data and 'temperature' in data['current']:
            temperatura = data['current']['temperature']
            return temperatura
        else:
            raise ValueError("Estructura inesperada de respuesta de API")

    except requests.exceptions.RequestException as e:
        print("Error en la solicitud de la API:", e)
        return None
    except ValueError as ve:
        print(ve)
        return None

def mapear_clima(temperatura):
    if temperatura > 25:
        return 'calido'
    elif 20 < temperatura <= 25:
        return 'tropical'
    elif 15 < temperatura <= 20:
        return 'templado'
    elif 5 < temperatura <= 15:
        return 'frio'
    else:
        return 'desértico'



def buscar_enfermedades_por_clima(clima, df):
    resultados = df[df['weather'] == clima]
    return resultados[['Disease', 'Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']]

url = 'https://github.com/OAGgithub/SIC-Python/blob/main/Python_Files/Dataset/Disease_symptom_and_patient_profile_dataset_with_weather.xlsx?raw=true'
df = pd.read_excel(url)

print(df.columns)

api_key = 'j7pntj6vhevorwpzb9tk9bl06gf5g84ek58iafb8'
localidad = 'azua'
temperatura_actual = obtener_temperatura(localidad, api_key)

if temperatura_actual is not None:
    print('Current temperature in {} is {} °C.'.format(localidad, temperatura_actual))

    clima_actual = mapear_clima(temperatura_actual)
    print('El clima actual es {}.'.format(clima_actual))

    enfermedades = buscar_enfermedades_por_clima(clima_actual, df)


    tabla_resultados = tabulate(enfermedades, headers='keys', tablefmt='fancy_grid')
    print(tabla_resultados)

    conteo_enfermedades = enfermedades['Disease'].value_counts()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=conteo_enfermedades.values, y=conteo_enfermedades.index, palette='viridis')
    plt.xlabel('Frecuencia')
    plt.ylabel('Enfermedades')
    plt.title('Frecuencia de Enfermedades según el Clima Actual')
    plt.show()
else:
    print("No se pudo obtener la temperatura actual.")