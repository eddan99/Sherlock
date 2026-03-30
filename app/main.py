from fastapi import FastAPI, HTTPException
from app.rag import RAG
from fastapi import UploadFile, File


app = FastAPI()
rag = RAG()

@app.post("/documents")
async def upload_documents(file: UploadFile = File(...)):
    try:
        await rag.ingest(file)
        return {"message": "Documents ingested successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query(question: str):
    try:
        answer = await rag.query(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
