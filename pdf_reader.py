from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def chunk_pdf(pdf_file, chunk_size=4000, overlap=1000):
    """
    Esta função divide o texto de um arquivo PDF em chunks.

    Args:
        pdf_file (str): Caminho para o arquivo PDF.
        chunk_size (int): Tamanho desejado para cada chunk de texto.
        overlap (int): Número de caracteres de sobreposição entre chunks consecutivos.

    Returns:
        list: Lista de chunks de texto.
    """

    chunks = []  # Lista para armazenar os chunks de texto
    chunk = ""  # String para armazenar o texto do chunk atual

    output_string = StringIO()
    with open(pdf_file, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    text = output_string.getvalue()

    # Divida o texto em chunks
    while len(text) > chunk_size:
        chunks.append(text[:chunk_size])
        text = text[chunk_size-overlap:]

    # Se houver algum texto restante, adicione-o à lista de chunks
    if len(text):
        chunks.append(text)

    return chunks