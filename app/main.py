from fastapi import FastAPI
from app.rag import RAG

app = FastAPI()
rag = RAG()

@app.post("/documents")
async def upload_documents():
        rag.ingest()
        return {"message": "Documents ingested successfully."}

@app.post("/query")
async def query(question: str):
    answer = await rag.query(question)
    return {"answer": answer}

