class TestApi:
    def test_list_uploaded_files(self, client):
        response = client.get("/documents")
        assert response.status_code == 200

    def test_query_without_documents(self, client):
        response = client.post("/query", json={"question": "who is spiderman?"})
        assert response.status_code == 200
        assert "enough evidence" in response.json()["answer"].lower()

    def test_ingest(self, client):
        with open("tests/nke-10k-2023.pdf", "rb") as f:
            response = client.post("/documents", files={"file": ("nke-10k-2023.pdf", f, "application/pdf")})
        assert response.status_code == 200

    def test_ingest_and_query(self, client):
        with open("tests/nke-10k-2023.pdf", "rb") as f:
            response = client.post("/documents", files={"file": ("nke-10k-2023.pdf", f, "application/pdf")})
        assert response.status_code == 200
        response = client.post("/query", json={"question": "how many employees does Nike have? Only answer in exact numbers. Example: 74,300"})
        assert response.status_code == 200
        assert "83,700" in response.json()["answer"]