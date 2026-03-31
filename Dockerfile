FROM python:3.13-slim AS builder
ARG GOOGLE_API_KEY
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY tests ./tests
RUN PYTHONPATH=/app pytest tests/

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app/app ./app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
RUN useradd app && mkdir -p ./chroma_langchain_db ./uploads && chown -R app:app ./chroma_langchain_db ./uploads
USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]