import io
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

# Cargar el modelo entrenado
with open('./diagnostic_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Cargar las columnas de síntomas del dataset original
df = pd.read_csv("./DiagnosticCare/Dataset/Diseases_Training.csv")
columns = df.drop(['prognosis', 'Unnamed: 133'], axis=1).columns

# region  Diccionario de sintomas 
symptom_translation = {
    "itching": "comezón",
    "skin_rash": "erupción cutánea",
    "nodal_skin_eruptions": "erupciones nodulares en la piel",
    "continuous_sneezing": "estornudos continuos",
    "shivering": "escalofríos",
    "chills": "escalofríos",
    "joint_pain": "dolor en las articulaciones",
    "stomach_pain": "dolor de estómago",
    "acidity": "acidez",
    "ulcers_on_tongue": "úlceras en la lengua",
    "muscle_wasting": "desgaste muscular",
    "vomiting": "vómitos",
    "burning_micturition": "ardor al orinar",
    "spotting_ urination": "micción con manchas",
    "fatigue": "fatiga",
    "weight_gain": "aumento de peso",
    "anxiety": "ansiedad",
    "cold_hands_and_feets": "manos y pies fríos",
    "mood_swings": "cambios de humor",
    "weight_loss": "pérdida de peso",
    "restlessness": "inquietud",
    "lethargy": "letargo",
    "patches_in_throat": "manchas en la garganta",
    "irregular_sugar_level": "nivel de azúcar irregular",
    "cough": "tos",
    "high_fever": "fiebre alta",
    "sunken_eyes": "ojos hundidos",
    "breathlessness": "dificultad para respirar",
    "sweating": "sudoración",
    "dehydration": "deshidratación",
    "indigestion": "indigestión",
    "headache": "dolor de cabeza",
    "yellowish_skin": "piel amarillenta",
    "dark_urine": "orina oscura",
    "nausea": "náuseas",
    "loss_of_appetite": "pérdida de apetito",
    "pain_behind_the_eyes": "dolor detrás de los ojos",
    "back_pain": "dolor de espalda",
    "constipation": "estreñimiento",
    "abdominal_pain": "dolor abdominal",
    "diarrhoea": "diarrea",
    "mild_fever": "fiebre leve",
    "yellow_urine": "orina amarilla",
    "yellowing_of_eyes": "ojos amarillentos",
    "acute_liver_failure": "insuficiencia hepática aguda",
    "fluid_overload": "sobrecarga de líquidos",
    "swelling_of_stomach": "hinchazón del estómago",
    "swelled_lymph_nodes": "ganglios linfáticos hinchados",
    "malaise": "malestar",
    "blurred_and_distorted_vision": "visión borrosa y distorsionada",
    "phlegm": "flema",
    "throat_irritation": "irritación de garganta",
    "redness_of_eyes": "enrojecimiento de los ojos",
    "sinus_pressure": "presión sinusal",
    "runny_nose": "nariz que moquea",
    "congestion": "congestión",
    "chest_pain": "dolor en el pecho",
    "weakness_in_limbs": "debilidad en las extremidades",
    "fast_heart_rate": "frecuencia cardíaca rápida",
    "pain_during_bowel_movements": "dolor durante los movimientos intestinales",
    "pain_in_anal_region": "dolor en la región anal",
    "bloody_stool": "heces con sangre",
    "irritation_in_anus": "irritación en el ano",
    "neck_pain": "dolor de cuello",
    "dizziness": "mareo",
    "cramps": "calambres",
    "bruising": "moretones",
    "obesity": "obesidad",
    "swollen_legs": "piernas hinchadas",
    "swollen_blood_vessels": "vasos sanguíneos hinchados",
    "puffy_face_and_eyes": "cara y ojos hinchados",
    "enlarged_thyroid": "tiroides agrandada",
    "brittle_nails": "uñas quebradizas",
    "swollen_extremeties": "extremidades hinchadas",
    "excessive_hunger": "hambre excesiva",
    "extra_marital_contacts": "contactos extra matrimoniales",
    "drying_and_tingling_lips": "labios secos y con hormigueo",
    "slurred_speech": "dificultad para hablar",
    "knee_pain": "dolor de rodilla",
    "hip_joint_pain": "dolor en la articulación de la cadera",
    "muscle_weakness": "debilidad muscular",
    "stiff_neck": "rigidez en el cuello",
    "swelling_joints": "articulaciones hinchadas",
    "movement_stiffness": "rigidez en el movimiento",
    "spinning_movements": "movimientos giratorios",
    "loss_of_balance": "pérdida de equilibrio",
    "unsteadiness": "inestabilidad",
    "weakness_of_one_body_side": "debilidad de un lado del cuerpo",
    "loss_of_smell": "pérdida del olfato",
    "bladder_discomfort": "malestar en la vejiga",
    "foul_smell_of urine": "olor desagradable de la orina",
    "continuous_feel_of_urine": "sensación continua de orinar",
    "passage_of_gases": "paso de gases",
    "internal_itching": "picazón interna",
    "toxic_look_(typhos)": "aspecto tóxico (tifo)",
    "depression": "depresión",
    "irritability": "irritabilidad",
    "muscle_pain": "dolor muscular",
    "altered_sensorium": "sensorio alterado",
    "red_spots_over_body": "manchas rojas en el cuerpo",
    "belly_pain": "dolor de barriga",
    "abnormal_menstruation": "menstruación anormal",
    "dischromic _patches": "parches discromicos",
    "watering_from_eyes": "lagrimeo",
    "increased_appetite": "aumento del apetito",
    "polyuria": "poliuria",
    "family_history": "historia familiar",
    "mucoid_sputum": "esputo mucoide",
    "rusty_sputum": "esputo oxidado",
    "lack_of_concentration": "falta de concentración",
    "visual_disturbances": "alteraciones visuales",
    "receiving_blood_transfusion": "recepción de transfusión de sangre",
    "receiving_unsterile_injections": "recepción de inyecciones no estériles",
    "coma": "coma",
    "stomach_bleeding": "sangrado estomacal",
    "distention_of_abdomen": "distensión del abdomen",
    "history_of_alcohol_consumption": "historia de consumo de alcohol",
    "fluid_overload": "sobrecarga de líquidos",
    "blood_in_sputum": "sangre en el esputo",
    "prominent_veins_on_calf": "venas prominentes en la pantorrilla",
    "palpitations": "palpitaciones",
    "painful_walking": "caminar doloroso",
    "pus_filled_pimples": "granos llenos de pus",
    "blackheads": "puntos negros",
    "scurring": "costras",
    "skin_peeling": "descamación de la piel",
    "silver_like_dusting": "polvo parecido a la plata",
    "small_dents_in_nails": "pequeñas abolladuras en las uñas",
    "inflammatory_nails": "uñas inflamatorias",
    "blister": "ampolla",
    "red_sore_around_nose": "llaga roja alrededor de la nariz",
    "yellow_crust_ooze": "costra amarilla supurante"
}
# endregion 

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  
    input_symptoms = data['symptoms']
    
    # Crear un DataFrame con los síntomas proporcionados
    input_data = np.zeros(len(columns))
    for symptom in input_symptoms:
        if symptom in columns:
            input_data[columns.get_loc(symptom)] = 1
    
    input_df = pd.DataFrame([input_data], columns=columns)
    
    
    probabilities = model.predict_proba(input_df)[0]
    
    # Obtener las 10 enfermedades con mayor probabilidad
    top_10_indices = probabilities.argsort()[-10:][::-1]
    top_10_diseases = [(model.classes_[i], probabilities[i]) for i in top_10_indices]
    
   
    diseases = [disease for disease, prob in top_10_diseases]
    # Transformar a porciento
    probs = [(prob * 100) for disease, prob in top_10_diseases]
    
    # Generar gráfico
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

@app.route('/getsymptoms', methods=['GET'])
def get_symptoms():
    # Crear un diccionario con los síntomas traducidos
    translated_symptoms = [{"english": symptom, "spanish": symptom_translation.get(symptom, symptom)} for symptom in columns]
    return jsonify(translated_symptoms)

if __name__ == '__main__':
    app.run(debug=True)
