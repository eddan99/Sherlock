from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import UploadFile, File
from dotenv import load_dotenv
import os
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

    async def ingest(self, file: UploadFile):
        os.makedirs("./uploads", exist_ok=True)
        file_path = os.path.join("./uploads", file.filename)

        content = await file.read()
        with open(file_path, "wb") as uploaded_file:
            uploaded_file.write(content)

        loader = PyPDFLoader(file_path)
        docs = loader.load()
        all_splits = self.text_splitter.split_documents(docs)
        self.vector_store.add_documents(documents=all_splits)

    async def query(self, question):
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3},
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{question}"),
        ])

        def format_docs(docs):
            return "\n\n".join(d.page_content for d in docs)

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        result = chain.invoke(question)
        return result
    
