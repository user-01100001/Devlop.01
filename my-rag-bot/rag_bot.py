from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

import os

# Load documents from .txt file
print("➡️ Loading: my-rag-bot/data/info.txt")
loader = TextLoader("my-rag-bot/data/info.txt", encoding="utf-8")
docs = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Create embeddings with LLaMA 3
embedding = OllamaEmbeddings(model="llama3")  # ✅ explicitly set model

# Create vector store
print("📦 Creating FAISS vector store...")
vectorstore = FAISS.from_documents(chunks, embedding=embedding)

# Load LLM
llm = Ollama(model="llama3")

# Retrieval QA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# Interactive Q&A
print("\n🤖 Ask me anything (type 'exit' to quit):")
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    answer = qa_chain.run(query)
    print("🧠 Answer:", answer)
