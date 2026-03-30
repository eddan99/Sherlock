from langchain_community.document_loaders import PyPDFLoader

file_path = "nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

print(len(docs))