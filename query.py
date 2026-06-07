from sentence_transformers import SentenceTransformer
import chromadb

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("nba_teams")

while True:
    query = input("\nAsk a question (or type quit): ")

    if query.lower() == "quit":
        break

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    print("\nTop Results:\n")

    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]

        print("=" * 60)
        print(f"Source: {source}")
        print(doc[:500])
        print()