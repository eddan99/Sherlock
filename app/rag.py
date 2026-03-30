from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import getpass
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


class RAG:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )
        self.vector_store = Chroma(
            collection_name="example_collection",
            embedding_function=self.embeddings,
            persist_directory="./chroma_langchain_db",        
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        self.llm = GoogleGenerativeAI(
            model="gemini-2.5-flash-lite", 
            temperature=0.0
        )
        self.system_prompt = """You are a really good assistant for answering questions based on a document.
            Use only the following context to answer the question.
            If the answer is not in the context, say: "I don't have enough evidence for that."
            Context: {context}"""

    def ingest(self):
        pass

    def query():
        pass