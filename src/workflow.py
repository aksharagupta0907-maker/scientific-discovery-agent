
import json
from pathlib import Path

from arxiv_fetcher import fetch_arxiv_papers
from agents.agents.literature_reviewer import review_paper
from agents.agents.hypothesis_generator import generate_hypotheses


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def run_workflow():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: Fetching research papers from arXiv...")
    papers = fetch_arxiv_papers(
        query="machine learning",
        max_results=5
    )

    if not papers:
        print("No papers fetched. Check your internet connection.")
        return

    print(f"Fetched {len(papers)} papers.")

    print("\nStep 2: Reviewing papers...")
    reviewed_papers = []

    for paper in papers:
        try:
            review = review_paper(paper)
            reviewed_papers.append(review)
        except Exception as error:
            print(f"Review failed: {error}")

    with (DATA_DIR / "reviewed_papers.json").open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(reviewed_papers, file, indent=4, ensure_ascii=False)

    print(f"Reviewed {len(reviewed_papers)} papers.")

    print("\nStep 3: Generating hypotheses...")
    hypotheses = generate_hypotheses(reviewed_papers)

    with (DATA_DIR / "hypotheses.json").open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(hypotheses, file, indent=4, ensure_ascii=False)

    print(f"Generated {len(hypotheses)} hypotheses.")
    print("\nWorkflow completed!")


if __name__ == "__main__":
    run_workflow()
