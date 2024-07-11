import io
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

# Cargar el modelo entrenado
with open('./DiagnosticCare/diagnostic_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Cargar las columnas de síntomas del dataset original
df = pd.read_csv("./DiagnosticCare/Dataset/Diseases_Training.csv")
columns = df.drop(['prognosis', 'Unnamed: 133'], axis=1).columns

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Suponiendo que los síntomas se envían en formato JSON
    input_symptoms = data['symptoms']
    
    # Crear un DataFrame con los síntomas proporcionados
    input_data = np.zeros(len(columns))
    for symptom in input_symptoms:
        if symptom in columns:
            input_data[columns.get_loc(symptom)] = 1
    
    input_df = pd.DataFrame([input_data], columns=columns)
    
    # Predecir las probabilidades de cada enfermedad
    probabilities = model.predict_proba(input_df)[0]
    
    # Obtener las 10 enfermedades con mayor probabilidad
    top_10_indices = probabilities.argsort()[-10:][::-1]
    top_10_diseases = [(model.classes_[i], probabilities[i]) for i in top_10_indices]
    
    # Generar el gráfico
    diseases = [disease for disease, prob in top_10_diseases]
    probs = [(prob * 100) for disease, prob in top_10_diseases]
    
    plt.figure(figsize=(10, 6))
    plt.barh(diseases, probs, color='skyblue')
    plt.xlabel('Probabilidad (%)')
    plt.title('Top 10 Enfermedades Probables')
    plt.gca().invert_yaxis()
    
    # Añadir etiquetas de porcentaje al eje x
    plt.xticks(np.arange(0, 101, 10), [f'{i}%' for i in range(0, 101, 10)])
    
    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Devolver el gráfico y los datos como JSON
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
