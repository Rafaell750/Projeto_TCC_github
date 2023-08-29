from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import logging

# Defina o nível de log para DEBUG
logging.basicConfig(level=logging.DEBUG)

# Dicionário com informações sobre multas e gravidades
multa_gravidade = {
    "leve": {
        "valor": 88.38,
        "pontos_na_cnh": 3
    },
    "média": {
        "valor": 130.16,
        "pontos_na_cnh": 4
    },
    "grave": {
        "valor": 195.23,
        "pontos_na_cnh": 5
    },
    "gravíssima": {
        "valor": 293.47,
        "pontos_na_cnh": 7,
        "fator_multiplicador": "x1 até x20"
    }
}

class ActionMultaGravidade(Action):
    def name(self) -> Text:
        return "action_multa_gravidade"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Importe o módulo de logging
        import logging

        # Defina o logger aqui
        logger = logging.getLogger(__name__)
        logger.debug("Inside action_multa_gravidade")

        # Obtém a intenção do usuário
        intent = tracker.latest_message["intent"].get("name")
        logger.debug(f"Intent: {intent}")

        if intent in multa_gravidade and "valor" in multa_gravidade[intent]:
            multa_info = multa_gravidade[intent]
            message = (
                f"O valor da multa de gravidade '{intent}' é R$ {multa_info['valor']}"
            )

        else:
            message = "Desculpe, não tenho informações sobre essa gravidade de multa."

        dispatcher.utter_message(text=message)
        return []


# # informações sobre pontuação na CNH
# class ActionPontuacaoCNH(Action):
#     def name(self) -> Text:
#         return "action_pontuação_cnh"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#      # Enviando a resposta previamente definida no arquivo responses.md
#         dispatcher.utter_message(text="utter_pontuação_cnh")
#         return []

# # Artigos

# class ActionArt162ao164(Action):
#     def name(self) -> Text:
#         return "action_art_162_ao_164"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         dispatcher.utter_message(response="utter_art_162_ao_164")
#         return []

# class ActionArt165AaoC(Action):
#     def name(self) -> Text:
#         return "action_art_165_A_ao_C"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         dispatcher.utter_message(text="utter_art_165_A_ao_C")
#         return []





# Resposta quando nenhuma intenção específica é identificada
# class ActionDefaultFallback(Action):
#     def name(self) -> Text:
#         return "action_default_fallback"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(template="utter_default")
#         return []


