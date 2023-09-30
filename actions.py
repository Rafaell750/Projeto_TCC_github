from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import requests
import re
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import json


class ActionFetchLei(Action):
    def name(self):
        return "action_fetch_lei"

    def run(self, dispatcher, tracker, domain):
        file_path = 'C:\\Users\\rafae\\Documents\\Rasa_Projects\\Projeto_TCC\\L9503.pdf'
        text = self.extract_text_from_pdf(file_path)

        # Obtenha a última mensagem do usuário (a pergunta)
        question = tracker.latest_message.get('text')

        # Use a função get_keywords para obter as palavras-chave da pergunta
        keywords = self.get_keywords(question)

        # Imprima as palavras-chave para depuração
        print("Palavras-chave:", keywords)

        # Verifique se cada palavra-chave está no texto
        for keyword in keywords:
            if keyword in text:
                print(f"A palavra-chave 'álcool' foi encontrada no texto.")
            else:
                print(f"A palavra-chave 'álcool' não foi encontrada no texto.")

        # Divida o texto em chunks de 5000 caracteres (ou o tamanho que preferir)
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]

        # Procure por palavras-chave em cada chunk e use a função answer_question para gerar uma resposta
        for chunk in chunks:
            if any(keyword in chunk for keyword in keywords):
                response = self.answer_question(chunk, question)
                if response.get("answer_found"):
                    dispatcher.utter_message(text=response.get("response"))
                    return [SlotSet("lei_info", response.get("response"))]

        dispatcher.utter_message(text='Desculpe, não consegui encontrar uma resposta para a sua pergunta.')
        return [SlotSet("lei_info", None)]

    def extract_text_from_pdf(self, file_path):
        output_string = StringIO()
        with open(file_path, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        return output_string.getvalue()

    def get_keywords(self, question):
        url = 'https://api.pawan.krd/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer pk-bYmcGbiKOqnbZJESVyOXEwyBhLtnxjEDlTTSVUmsknzcRgkG',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "gpt-3.5-turbo",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        return response.json()

    def answer_question(self, chunk, question):
        url = 'https://api.pawan.krd/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer pk-bYmcGbiKOqnbZJESVyOXEwyBhLtnxjEDlTTSVUmsknzcRgkG',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "gpt-3.5-turbo",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "system",
                    "content": chunk
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        return response.json()