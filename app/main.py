from fastapi import FastAPI
from rag import RAG

app = FastAPI()
rag = RAG()

@app.post("/documents")
async def root():
    return {"message": "Hello World"}

@app.post("/query")
async def query():
    answer = await rag.query("how many employees does Nike have?")
    return {"answer": answer}

