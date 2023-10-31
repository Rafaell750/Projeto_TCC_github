from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from texto_pdf import texto
import openai

# API
openai.api_key = 'pk-jgZhazuvwcXjvflTexuwKNVqpiVFkMxAyqtYigqZBrdfJnIa'
openai.api_base = 'https://api.pawan.krd/v1'
model = "pai-001-light-beta"

# Ação personalizada para obter palavras-chave
class ActionGetKeywords(Action):
    def name(self):
        return "action_get_keywords"

    def run(self, dispatcher, tracker, domain):
        question = tracker.latest_message['text']
        
        # Definindo o prompt para a chamada da API
        prompt = f"""Respoda as perguntas ao encontrar a informação para a pergunta em um arquivo texto_pdf.py. Oberve a pergunta do usuario e busque por palavras chaves no texto_pdf.py para responder a mesma. Apenas uma palavra por palavra-chave. Use apenas letras minúsculas. 
    
{question}"""
        # Fazendo a chamada da API
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Você sempre fornecerá 8 palavras-chave que incluam sinônimos relevantes das palavras da pergunta original."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.1,  # Tornar as respostas mais focadas
            max_tokens=100,  # Permitir respostas mais longas
        )
        arguments = response["choices"][0]["message"]["content"].lower()
        keywords = arguments.split(", ")

        return [SlotSet("keywords", keywords)]

# Ação personalizada para responder à pergunta
class ActionAnswerQuestion(Action):
    def name(self):
        return "action_answer_question"

    def run(self, dispatcher, tracker, domain):
        # Obtendo a última mensagem do usuário e o valor do slot keywords
        question = tracker.latest_message['text']
        keywords = tracker.get_slot('keywords')
        
         # Definindo o prompt para a chamada da API
        prompt = f"""```
{texto}

{question}
```"""
        # Fazendo a chamada da API
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Responda somente em portugues. Always set answer_found to false if the answer to the question was not found in the informaton provided."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.1,  # Tornar as respostas mais focadas
            max_tokens=200,  # Permitir respostas mais longas
            functions=[
                {
                    "name": "give_response",
                    "description": "Use this function to give the response and whether or not the answer to the question was found in the text.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "answer_found": {
                                "type": "boolean",
                                "description": "Set this to true only if the provided text includes an answer to the question"
                            },
                            "response": {
                                "type": "string",
                                "description": "The full response to the question, if the information was relevant"
                            }
                        }
                    },
                    "required": ["answer_found"]
                }
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        
        # Enviando a resposta para o usuário
        dispatcher.utter_message(answer)

        # Armazenando a última pergunta feita pelo usuário e a última resposta dada pelo bot
        return [SlotSet("last_question", question), SlotSet("last_answer", answer), SlotSet("keywords", keywords)]