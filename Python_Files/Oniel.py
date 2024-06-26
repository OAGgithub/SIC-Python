import pandas as pd

file_path = './Dataset/Disease_symptom_and_patient_profile_dataset_updated.xlsx'
df = pd.read_excel(file_path)

class EnfermedadesDF:
    def __init__(self, dataframe):
        self.df = dataframe

    def search_by_name(self, name):
        # Busca enfermedades por su nombre
        return self.df[self.df['Disease'].str.contains(name, case=False, na=False)]

    def get_all(self):
        
        # Selecciona todas las enfermedades
        return self.df['Disease'].unique()

    def select_number_of_diseases(self, names, number):
        
        # Selecciona un número de enfermedades por nombre.
        filtered_df = self.df[self.df['Disease'].isin(names)]
        return filtered_df.head(number)

    def filter_diseases(self, **filters):
        
        # Filtra enfermedades basado en criterios específicos
        filtered_df = self.df.copy()
        for key, value in filters.items():
            if key in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[key] == value]
        return filtered_df


data = EnfermedadesDF(df)


# PRUEBA DE FUNCIONES  ( BORRAR DESPUES     )


disease_name_search = data.search_by_name('Asthma')

all_diseases = data.get_all()

selected_diseases = data.select_number_of_diseases(['Asthma', 'Influenza'], 2)

filtered_diseases = data.filter_diseases(Gender='Female', Outcome='Positive')

# Resultados
print(disease_name_search.head())
print(all_diseases)
print(selected_diseases)
print(filtered_diseases.head())
