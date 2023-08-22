from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# Informações sobre multas e gravidade
class ActionMultaGravidade(Action):
    def name(self) -> Text:
        return "action_multa_gravidade"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = (
            "Segue abaixo as informações sobre as multas:\n"
            "Infração leve: R$ 88,38 - pontos na CNH: 3\n"
            "Infração média: R$ 130,16 - pontos na CNH: 4\n"
            "Infração grave: R$ 195,23 - pontos na CNH: 5\n"
            "Infração gravíssima: R$ 293,47 - pontos na CNH: 7\n"
            "OBS: Infração gravíssima possuem o fator multiplicador variando de acordo com a infração cometida, podendo ir de x1 até x20 o valor\n"
        )
        
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


