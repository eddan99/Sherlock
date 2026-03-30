from fastapi import FastAPI, HTTPException
from app.rag import RAG
from fastapi import UploadFile, File
from app.schemas import QueryRequest

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
async def query(request: QueryRequest):
    try:
        answer = await rag.query(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def uploaded_files():
    return rag.list_uploaded_files()