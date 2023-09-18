import requests
from bs4 import BeautifulSoup
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

import PyPDF2
import re

class ActionFetchLei(Action):
    def name(self):
        return "action_fetch_lei"

    def run(self, dispatcher, tracker, domain):
        file_path = 'C:\\Users\\rafae\\Documents\\Rasa_Projects\\Projeto_TCC\\L9503.pdf'
        text = self.extract_text_from_pdf(file_path)

        # Definir palavras-chaves
        keywords = ['álcool']

        # Divide o texto em sentenças
        sentences = re.split('(?<=[.!?]) +', text)

        # Procure por palavras-chave no texto
        relevant_sentences = [sentence for sentence in sentences if any(keyword in sentence for keyword in keywords)]

        if relevant_sentences:
            # Se alguma palavra-chave for encontrada, envie uma mensagem com as sentenças relevantes
            dispatcher.utter_message(text=' '.join(relevant_sentences))
        else:
            # Se nenhuma palavra-chave for encontrada, envie uma mensagem diferente
            dispatcher.utter_message(text='Nenhuma das palavras-chave procuradas foi encontrada no texto.')

        return [SlotSet("lei_info", text)]

    def extract_text_from_pdf(self, file_path):
        pdf_file_obj = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        num_pages = len(pdf_reader.pages)
        text = ""
        for page in range(num_pages):
            page_obj = pdf_reader.pages[page]
            text += page_obj.extract_text()
        pdf_file_obj.close()
        return text

