import streamlit as st
import fitz
from groq import Groq
import os

# Caminho dinâmico da imagem
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")   

# Caminho para a pasta dos PDFs
PDF_DIR = os.path.join(CURRENT_DIR, "pdfs")  # Defina o diretório onde os PDFs estão

# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Função para extrair os arquivos
def extract_files_from_directory(directory):
    text = ""
    # Percorre todos os arquivos PDF na pasta
    for pdf_file in os.listdir(directory):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(directory, pdf_file)
            with fitz.open(pdf_path) as doc: 
                for page in doc:
                    text += page.get_text("text") 
    return text

# Motor de inferência para o sistema inteligente
def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente de Diagnóstico de Doenças que responde com base em documentos fornecidos sobre quais são os melhores lugares e pontos para visitar."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content    

# CRIAR A INTERFACE
def main():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(LOGO_PATH, width=200)
    with col2:
        st.title("Diagnóstico de Doenças")

    # Caixa de entrada da pergunta - visível desde o início
    user_input = st.text_input("Digite a sua pergunta:")

    # Carregar e extrair os PDFs automaticamente da pasta
    text = extract_files_from_directory(PDF_DIR)
    st.session_state["document-text"] = text

    if user_input:
        # Quando o texto do PDF for extraído, exibe a resposta
        st.write("Resposta do Agente:")
        st.write(chat_with_groq(user_input, text))

if __name__ == "__main__":
    main()
