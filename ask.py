from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client_groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

client_chroma = chromadb.PersistentClient(path="chroma_db")
collection = client_chroma.get_collection("nba_teams")

while True:
    question = input("\nAsk a question (or type quit): ")

    if question.lower() == "quit":
        break

    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_docs = results["documents"][0]
    retrieved_sources = [
        meta["source"]
        for meta in results["metadatas"][0]
    ]

    context = "\n\n".join(retrieved_docs)

    prompt = f"""
You are an NBA analyst.

Answer the question using ONLY the provided context.

If the answer is not contained in the context, say:
"I could not find enough information in the retrieved documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    print("\nANSWER")
    print("-" * 50)
    print(answer)

    print("\nSOURCES")
    print("-" * 50)

    for source in set(retrieved_sources):
        print(source)