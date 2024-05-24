from flask import Flask, request, render_template
import requests
from PyPDF2 import PdfReader
import google.generativeai as genai

genai.configure(api_key="AIzaSyASX8v2KKXP0OAAlHrYXHns0swN7Xvn_nQ")
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = ""
        if 'pdf' in request.files and request.files['pdf'].filename != '':
            pdf_file = request.files['pdf']
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()

        user_input = request.form['question']
        if not user_input.strip() and not text.strip():
            return "Debes enviar al menos una pregunta o un PDF."

        chat = model.start_chat(history=[])
        if user_input.strip():
            response = chat.send_message(user_input, stream=True)
            response.resolve()
            answer = response.parts[0].text
        else:
            answer = ""

        return render_template('index.html', answer=answer)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
