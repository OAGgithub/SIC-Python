from flask import Flask, render_template, request
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from models import EnfermedadesDF, obtener_temperatura, mapear_clima, buscar_enfermedades_por_clima

app = Flask(__name__)

# URL del dataset de enfermedades
url_enfermedades = 'https://github.com/OAGgithub/SIC-Python/blob/main/Python_Files/Dataset/Disease_symptom_and_patient_profile_dataset_updated.xlsx?raw=true'
df_enfermedades = pd.read_excel(url_enfermedades)

# URL del dataset con información climática
url_clima_enfermedades = 'https://github.com/OAGgithub/SIC-Python/blob/main/Python_Files/Dataset/Disease_symptom_and_patient_profile_dataset_with_weather.xlsx?raw=true'
df_clima_enfermedades = pd.read_excel(url_clima_enfermedades)

# Instanciar la clase EnfermedadesDF para trabajar con los datos de enfermedades
data = EnfermedadesDF(df_enfermedades)

# Rutas de la aplicación Flask
@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/analisis')
def analisis():
    return render_template('Analisis.html')

@app.route('/catalogo')
def catalogo():
    return render_template('Catalogo.html')

@app.route('/basico')
def catalogo():
    return render_template('Basico.html')

@app.route('/Profundo')
def catalogo():
    return render_template('Profundo.html')

@app.route('/informacion')
def informacion():
    return render_template('Informacion.html')

@app.route('/buscar_enfermedad', methods=['POST'])
def buscar_enfermedad():
    nombre_enfermedad = request.form['nombre_enfermedad']
    resultados = data.search_by_name(nombre_enfermedad)
    tabla_resultados = tabulate(resultados, headers='keys', tablefmt='fancy_grid')
    return render_template('Resultados.html', tabla_resultados=tabla_resultados)

@app.route('/analizar_clima')
def analizar_clima():
    api_key = 'j7pntj6vhevorwpzb9tk9bl06gf5g84ek58iafb8'
    localidad = 'azua'
    temperatura_actual = obtener_temperatura(localidad, api_key)

    if temperatura_actual is not None:
        clima_actual = mapear_clima(temperatura_actual)
        enfermedades = buscar_enfermedades_por_clima(clima_actual, df_clima_enfermedades)

        conteo_enfermedades = enfermedades['Disease'].value_counts()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=conteo_enfermedades.values, y=conteo_enfermedades.index, palette='viridis')
        plt.xlabel('Frecuencia')
        plt.ylabel('Enfermedades')
        plt.title('Frecuencia de Enfermedades según el Clima Actual')
        plt.savefig('static/Imagenes/frecuencia_enfermedades_clima.png')  # Guardar gráfico como archivo estático
        return render_template('Analisis.html', clima_actual=clima_actual)

    else:
        return "No se pudo obtener la temperatura actual."

if __name__ == '__main__':
    app.run(debug=True)
