import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://github.com/OAGgithub/SIC-Python/blob/main/Python_Files/Dataset/Disease_symptom_and_patient_profile_dataset_updated.xlsx?raw=true'
df = pd.read_excel(url)

print(df.columns)

def buscar_enfermedades(sintomas):
    mask = pd.Series([True] * len(df))

    columnas_sintomas = {
        'fever': 'Fever',
        'cough': 'Cough',
        'fatigue': 'Fatigue',
        'difficulty breathing': 'Difficulty Breathing'
    }

    for sintoma in sintomas:
        col = columnas_sintomas.get(sintoma.lower())
        if col:
            mask = mask & df[col].astype(str).str.contains('Yes', case=False, na=False)


    resultados = df[mask]

    return resultados[['Disease', 'Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']]


# Prueba
sintomas_entrada = ['fever', 'cough']
enfermedades = buscar_enfermedades(sintomas_entrada)

# Tabla de resultados
tabla_resultados = tabulate(enfermedades, headers='keys', tablefmt='fancy_grid')
print(tabla_resultados)

# Contar las enfermedades más frecuentes
conteo_enfermedades = enfermedades['Disease'].value_counts()

# Crear el histograma
plt.figure(figsize=(10, 6))
sns.barplot(x=conteo_enfermedades.values, y=conteo_enfermedades.index, palette='viridis')
plt.xlabel('Frecuencia')
plt.ylabel('Enfermedades')
plt.title('Frecuencia de Enfermedades según los Síntomas Proporcionados')
plt.show()