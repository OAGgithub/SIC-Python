from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

class ActionCheckMedicalResult(Action):
    def name(self) -> Text:
        return "action_check_medical_result"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        file_path = '/Users/oliverabreumateo/Downloads/R/Results.xlsx'
        
        df = pd.read_excel(file_path)
        
        for i, row in df.iterrows():
            dispatcher.utter_message(text=(str(row['ID']) + " " + str(row['Title'])))
        
        return []
