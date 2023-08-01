from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionMultaGravidade(Action):
    def name(self) -> Text:
        return "action_multa_gravidade"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = "Segue abaixo as informações sobre as infrações:\n\n"
        message += "Infração leve: R$ 88,38 - pontos na CNH: 3\n"
        message += "Infração média: R$ 130,16 - pontos na CNH: 4\n"
        message += "Infração grave: R$ 195,23 - pontos na CNH: 5\n"
        message += "Infração gravíssima: R$ 293,47 - pontos na CNH: 7\n"
        message += "OBS: Infração gravíssima possuem o fator multiplicador variando de acordo com a infração cometida, podendo ir de x2 até x20 o valor\n"

        dispatcher.utter_message(text=message)
        return []

class ActionPontuacaoCNH(Action):
    def name(self) -> Text:
        return "action_pontuacao_cnh"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="A CNH possui um limite de 20 pontos. Quando o condutor atinge esse limite, sua habilitação é suspensa.")
        return []


# Resposta quando nenhuma intenção específica é identificada
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_default")
        return []
