import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader  # For reading PDF content
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from io import BytesIO  # Import BytesIO to handle the byte stream from the file uploader

load_dotenv()

# Google Gemini API configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_txt(pdf_docs):
    """Extracts text from uploaded PDFs."""
    text = ""
    for pdf in pdf_docs:
        # Use BytesIO to wrap the bytes returned by the file uploader
        pdf_stream = BytesIO(pdf.read())
        pdf_reader = PdfReader(pdf_stream)
        for page in pdf_reader.pages:
            text += page.extract_text()  # Extract text from each page
    return text

def get_text_chunks(text):
    """Splits extracted text into chunks for vector storage."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    """Embeds text chunks and stores them in FAISS."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")  # Ensure this step completes

def get_conversational_chain():
    """Builds the conversational QA chain."""
    prompt_template = """
    You are an expert in reading, analyzing, and extracting meaningful information from PDF documents.
    You have the ability to understand and summarize the content, including technical documents, research papers,
    contracts, manuals, reports, and any other text-heavy document. Your task is to assist the user by:

    1. Summarizing sections or the entire document.
    2. Extracting key information based on user queries.
    3. Answering specific questions about the content.
    4. Providing insights and analysis on the topics discussed in the document.

    Context: \n {context}? \n
    Question: \n {question} \n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    """Handles user questions and searches in the FAISS vector store."""
    index_path = "faiss_index"
    
    if not os.path.exists(f"{index_path}/index.faiss"):
        st.error("FAISS index not found. Please upload and process a PDF first.")
        return None

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]

# Main function to tie everything together
def main():
    st.set_page_config(page_title="PDF Document QA with Google Gemini")  # Correct usage of set_page_config
    st.title("PDF Document QA with Google Gemini")
    
    # Sidebar for PDF file upload
    with st.sidebar:
        st.title("Navigation")
        pdf_docs = st.file_uploader("Upload your PDF files", type=["pdf"], accept_multiple_files=True)
        
        if st.button("Submit and PROCESS"):
            if pdf_docs:  # Check if files are uploaded
                with st.spinner("Processing..."):
                    raw_txt = get_pdf_txt(pdf_docs)
                    text_chunks = get_text_chunks(raw_txt)
                    get_vector_store(text_chunks)
                    st.success("Processing complete!")
            else:
                st.error("Please upload at least one PDF file.")
    
    # Main section for user question input
    user_question = st.text_input("Ask a question about the PDF content:")
    
    if user_question:
        response = user_input(user_question)
        if response:
            st.write(response)

# Run the main function
if __name__ == "__main__":
    main()


