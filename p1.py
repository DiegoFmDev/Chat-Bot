import pdfplumber
import nltk
from gensim.summarization import summarize

def analyze_pdf(pdf_path):
    """
    Analiza un PDF y genera un resumen a partir de su estructura.

    Args:
        pdf_path (str): Ruta al archivo PDF.

    Returns:
        str: Resumen del contenido del PDF.
    """

    with pdfplumber.open(pdf_path) as pdf:
        # Extraer información de la página
        page = pdf.pages[0]

        # Extraer texto de títulos, encabezados y párrafos
        text = []
        for element in page.extract_text():
            if isinstance(element, str):
                text.append(element)

        # Preprocesamiento del texto
        processed_text = " ".join(text)
        processed_text = processed_text.lower()
        processed_text = nltk.word_tokenize(processed_text)

        # Eliminar palabras irrelevantes
        stop_words = nltk.corpus.stopwords.words('english')
        processed_text = [word for word in processed_text if word not in stop_words]

        # Generar resumen
        summary = summarize(' '.join(processed_text), word_count=50)

    return summary

# Ejemplo de uso
pdf_path = "mi_archivo.pdf"
summary = analyze_pdf(pdf_path)
print(summary)
