# Sherlock

A RAG-based document Sherlock assistant. Upload PDF documents and ask questions, answers are strictly grounded in the provided documents using Retrieval Augmented Generation.

## Architecture

When a document is uploaded, it is split into chunks and converted into vector embeddings using Google Gemini. The embeddings are stored in a Chroma vector database. When a question is asked, the most relevant chunks are retrieved and passed as context to the LLM. A second LLM call (judge) then validates that the answer is grounded in the retrieved context before returning it to the user.

```
PDF upload  →  chunking  →  embeddings  →  Chroma vector store
                                                    ↓
User question  →  similarity search  →  context  →  LLM  →  judge  →  answer
```

## Project Structure

```
sherlock/
├── app/
│   ├── main.py        # FastAPI app and endpoints
│   ├── rag.py         # RAG pipeline (ingest, query, judge)
│   ├── config.py      # Configuration via pydantic-settings
│   └── schemas.py     # Request/response models
├── tests/
│   ├── conftest.py    # pytest fixtures
│   └── test_api.py    # API tests
├── frontend/          # React + Vite frontend
├── Dockerfile         # Multi-stage build (test + production)
├── docker-compose.yml
├── requirements.txt
└── .env               # Not committed — contains API key
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) — install and make sure it is running before proceeding
- A Google Gemini API key — get one at [aistudio.google.com](https://aistudio.google.com)

### Installing

1. Open a terminal:
   - **Windows (CMD):** Press `Win + R`, type `cmd`, press Enter
   - **Windows (PowerShell):** Run `ni .env` in the terminal, then open it with Notepad
   - **Mac:** Press `Cmd + Space`, type `Terminal`, press Enter

2. Clone the repository:
   ```
   git clone https://github.com/eddan99/sherlock.git
   ```

3. Navigate into the project folder:
   ```
   cd sherlock
   ```

4. Create a `.env` file in the root of the project folder:
   - **Windows:** Run `copy NUL .env` in the terminal, then open it with Notepad
   - **Mac:** Run `touch .env && open .env` in the terminal
   - Or right-click in your file explorer and create a new file named `.env`

   Add the following line to the file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
   Replace `your_api_key_here` with your actual Gemini API key.

   > **Note:** The `.env` file is listed in `.gitignore` and will never be committed to the repository.

5. Make sure Docker Desktop is open and running (you should see the Docker icon in your taskbar/menu bar).

6. Build and start the application:
   ```
   docker compose up --build
   ```
   The first build may take a few minutes. When you see `Application startup complete`, it is ready.

7. Open your browser and go to:
   ```
   http://localhost:4173
   ```

### API Endpoints

The backend API is available at `http://localhost:8000`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/documents` | Upload a PDF to the knowledge base |
| `POST` | `/query` | Ask a question based on uploaded documents |
| `GET` | `/documents` | List all uploaded documents |

### Tests

The test suite covers the three API endpoints:

- `POST /documents` — uploading a PDF
- `POST /query` — asking a question
- `GET /documents` — listing uploaded files

Tests run automatically during the Docker build.

To run them locally, activate the virtual environment from the root of the project:

**Windows:**
```
venv\Scripts\activate
pytest tests/
```

**Mac:**
```
source venv/bin/activate
pytest tests/
```

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) — REST API framework
- [LangChain](https://www.langchain.com/) — RAG pipeline
- [Chroma](https://www.trychroma.com/) — vector store
- [Google Gemini](https://ai.google.dev/) — LLM and embeddings
- [React](https://react.dev/) + [Vite](https://vitejs.dev/) — frontend

## Authors

- Edvin
