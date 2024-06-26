from flask import Flask, request, render_template
from PyPDF2 import PdfReader
import google.generativeai as genai
import nltk
import re
import numpy as np
import networkx as nx 

genai.configure(api_key="AIzaSyASX8v2KKXP0OAAlHrYXHns0swN7Xvn_nQ")
question_answering_model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['question']
        answer = ""

        if user_input.strip():  # Handle question answering
            chat = question_answering_model.start_chat(history=[])
            response = chat.send_message(user_input, stream=True)
            response.resolve()
            answer = response.parts[0].text

        elif 'pdf' in request.files and request.files['pdf'].filename != '':  # Handle PDF processing
            pdf_file = request.files['pdf']
            extracted_text = extract_text_from_pdf(pdf_file)
            if extracted_text:
                summary = summarize_pdf(extracted_text)
                summary = f"**Resumen del PDF:** {summary}"

                ai_analysis = ai_process_text(extracted_text)
                ai_analysis = f"\n\n**Análisis de IA:** {ai_analysis}"

                answer = summary + ai_analysis
            else:
                answer = "Error procesando PDF: Texto no extraído correctamente."

        else:
            answer = "Debes enviar al menos una pregunta o un PDF."
        
        return render_template('index.html', answer=answer)

    return render_template('index.html')

def extract_text_from_pdf(pdf_file):
            try:
                pdf_reader = PdfReader(pdf_file)
                extracted_text = ''

                for page in pdf_reader.pages:
                    extracted_text += page.extract_text()

                return extracted_text.strip()
            except Exception as e:
                print(f"Error extrayendo texto del PDF: {e}")
                return None
                # **Handle question answering if user input is present**
                # ... (Implement question answering using GenerativeAI or other methods)
                # **Improved summarization approach (consider these options):**
                # 1. Google GenerativeAI Summarization (if available)
                #    answer = summarize_pdf_using_generativeai(extracted_text)
                # 2. External Summarization API (e.g., Hugging Face Transformers)
                #    answer = summarize_pdf_using_external_api(extracted_text)
                # 3. TextRank-based summarization (using nltk)
                #    answer = summarize_pdf_using_textrank(extracted_text)  # Replace with your implementation

                if extracted_text.strip():
                    answer = summarize_pdf(extracted_text)  # Placeholder for your chosen summarization function

# **Define the chosen summarization function (replace with your implementation):**
def summarize_pdf(text):
    processed_text = nltk.word_tokenize(nltk.clean_tokens(text.lower()))
    sentence_similarity_matrix = nltk.metrics.jaccard_distance(nltk.ngrams(processed_text, 2))
    graph = nx.Graph()
    graph.add_nodes_from(range(len(processed_text)))
    for i, j, similarity in np.nditer(sentence_similarity_matrix):
        if i != j and similarity > 0.5:
            graph.add_edge(i, j)
    textrank = nltk.centrality.pagerank(graph)
    top_sentences = sorted(textrank.items(), key=lambda x: x[1], reverse=True)[:3]
    summary = []
    for _, sentence_id in top_sentences:
        summary.append(processed_text[sentence_id])
    return " ".join(summary)

def ai_process_text(text):
    # Replace this with your specific AI processing function
    # This is just a placeholder
    return f"Análisis de IA realizado en el texto: {text}"
 
if __name__ == '__main__':
    app.run(debug=True)
