from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

DATA_DIR = Path("data")


def load_documents():
    docs = []

    for file_path in DATA_DIR.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        docs.append({
            "source": file_path.name,
            "text": text
        })

    return docs


def chunk_text(text):
    chunks = []

    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE

        chunks.append(text[start:end])

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


print("Loading documents...")
documents = load_documents()

all_chunks = []

for doc in documents:
    chunks = chunk_text(doc["text"])

    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "id": f"{doc['source']}_{i}",
            "source": doc["source"],
            "text": chunk
        })

print(f"Created {len(all_chunks)} chunks")

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")
embeddings = model.encode(
    [c["text"] for c in all_chunks]
).tolist()

print("Creating Chroma database...")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="nba_teams"
)

collection.add(
    ids=[c["id"] for c in all_chunks],
    documents=[c["text"] for c in all_chunks],
    metadatas=[
        {"source": c["source"]}
        for c in all_chunks
    ],
    embeddings=embeddings
)

print("Done!")
print(f"Stored {len(all_chunks)} chunks")