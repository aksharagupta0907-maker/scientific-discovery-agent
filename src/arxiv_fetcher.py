
import requests
import feedparser
import json
from pathlib import Path


ARXIV_API_URL = "https://export.arxiv.org/api/query"

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_FILE = DATA_DIR / "arxiv_papers.json"


def fetch_arxiv_papers(query="machine learning", max_results=5):
    """Fetch recent research papers from arXiv."""

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    try:
        response = requests.get(
            ARXIV_API_URL,
            params=params,
            timeout=30,
        )
        response.raise_for_status()

        feed = feedparser.parse(response.content)
        papers = []

        for entry in feed.entries:
            paper = {
                "title": " ".join(entry.title.split()),
                "summary": " ".join(entry.summary.split()),
                "authors": [
                    author.name for author in entry.authors
                ],
                "published": entry.published,
                "url": entry.link,
            }
            papers.append(paper)

        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with OUTPUT_FILE.open("w", encoding="utf-8") as file:
            json.dump(papers, file, indent=4, ensure_ascii=False)

        print(f"Successfully fetched {len(papers)} papers.")
        print(f"Saved to: {OUTPUT_FILE}")

        return papers

    except (requests.RequestException, ValueError) as error:
        print(f"Could not fetch papers: {error}")
        return []


if __name__ == "__main__":
    fetch_arxiv_papers("machine learning", max_results=5)
