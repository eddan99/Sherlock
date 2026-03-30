from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from fastapi import UploadFile, File
from app.config import Settings
import os

settings = Settings()

class RAG:
    def __init__(self):
        os.environ["GOOGLE_API_KEY"] = settings.google_api_key
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model
        )
        self.vector_store = Chroma(
            collection_name=settings.collection_name,
            embedding_function=self.embeddings,
            persist_directory=settings.chroma_path,        
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        self.llm = GoogleGenerativeAI(
            model=settings.llm_model, 
            temperature=0.0
        )
        self.system_prompt = """You are a really good assistant for answering questions based on a document.
            Use only the following context to answer the question.
            If the answer is not in the context, say: "I don't have enough evidence for that."
            Context: {context}"""
        
        self.judge_prompt = """You are a judge. Given a question, context and answer, 
        respond with only 'GROUNDED' or 'NOT_GROUNDED' depending on whether the answer 
        is based on the context."""


    async def ingest(self, file: UploadFile):
        os.makedirs(settings.upload_folder, exist_ok=True)
        file_path = os.path.join(settings.upload_folder, file.filename)

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

        docs = retriever.invoke(question)
        context = "\n\n".join(d.page_content for d in docs)

        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{question}"),
        ])

        result = (prompt | self.llm | StrOutputParser()).invoke({"context": context, "question": question})

        return self.judge(question, context, result)

    def judge(self, question, context, answer):
        judge_prompt = ChatPromptTemplate.from_messages([
            ("system", self.judge_prompt),
            ("human", "Question: {question}\nContext: {context}\nAnswer: {answer}")
        ])
        decision_from_judge = (judge_prompt | self.llm | StrOutputParser()).invoke({
            "question": question,
            "context": context,
            "answer": answer
        })
        if "NOT_GROUNDED" in decision_from_judge.upper():
            return "I don't have enough evidence to answer that."
        return answer
    
    def list_uploaded_files(self):
        uploads_dir = settings.upload_folder
        if not os.path.exists(uploads_dir):
            return []   
        return os.listdir(uploads_dir)