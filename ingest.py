from pathlib import Path

DATA_DIR = Path("data")

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100


def load_documents():
    documents = []

    for file_path in DATA_DIR.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents


def chunk_text(text):
    chunks = []

    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE

        chunks.append(text[start:end])

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


if __name__ == "__main__":
    docs = load_documents()

    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })

    print(f"\nTotal chunks: {len(all_chunks)}\n")

    for chunk in all_chunks[:5]:
        print("=" * 50)
        print(chunk["source"])
        print(chunk["text"])
        print()