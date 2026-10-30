
import json
from pathlib import Path

import chromadb


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "all_research_papers.json"
DB_DIR = BASE_DIR / "data" / "chroma_db"


def local_embedding(text):
    vector = [0.0] * 128

    for word in text.lower().split():
        index = sum(ord(char) for char in word) % 128
        vector[index] += 1.0

    norm = sum(value * value for value in vector) ** 0.5

    if norm:
        vector = [value / norm for value in vector]

    return vector


class LocalEmbeddingFunction:
    def __call__(self, input):
        return [local_embedding(text) for text in input]

    @staticmethod
    def name():
        return "local_simple_embedding"

    @staticmethod
    def build_from_config(config):
        return LocalEmbeddingFunction()

    def get_config(self):
        return {}


def get_collection():
    client = chromadb.PersistentClient(path=str(DB_DIR))

    return client.get_or_create_collection(
        name="research_papers",
        embedding_function=LocalEmbeddingFunction(),
    )


def build_rag_database():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Research papers file not found: {DATA_FILE}"
        )

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        papers = json.load(file)

    if isinstance(papers, dict):
        papers = papers.get("papers", [])

    if not isinstance(papers, list):
        raise ValueError("Research papers data must be a list.")

    collection = get_collection()

    ids = []
    documents = []
    metadatas = []

    for index, paper in enumerate(papers):
        if not isinstance(paper, dict):
            continue

        title = str(paper.get("title", "Untitled paper"))
        abstract = str(paper.get("abstract") or "")
        summary = str(paper.get("summary") or "")

        document = (
            f"Title: {title}\n"
            f"Abstract: {abstract}\n"
            f"Summary: {summary}"
        ).strip()

        paper_id = str(
            paper.get("id")
            or f"{paper.get('source', 'paper')}_{index}"
        )

        ids.append(paper_id)
        documents.append(document)
        metadatas.append({
            "title": title,
            "source": str(paper.get("source", "unknown")),
        })

    if not documents:
        print("No research papers found.")
        return

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    print("\nRAG database ready!")
    print(f"Papers processed: {len(documents)}")
    print(f"Total papers in database: {collection.count()}")
    print(f"Database location: {DB_DIR}")


def search_papers(query, n_results=3):
    collection = get_collection()
    total = collection.count()

    if total == 0:
        print("Database is empty. Run the database builder first.")
        return ""

    results = collection.query(
        query_embeddings=[local_embedding(query)],
        n_results=min(n_results, total),
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    print(f"\nSearch query: {query}\n")

    for index, document in enumerate(documents, start=1):
        metadata = metadatas[index - 1] if index - 1 < len(metadatas) else {}

        print(f"{index}. {metadata.get('title', 'Untitled paper')}")
        print(document[:400])
        print("-" * 50)

    return "\n\n".join(documents)


if __name__ == "__main__":
    build_rag_database()
