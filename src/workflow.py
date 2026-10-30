
import json
from pathlib import Path

from arxiv_fetcher import fetch_arxiv_papers
from pubmed_fetcher import fetch_pubmed_papers
from agents.agents.literature_reviewer import review_paper
from agents.agents.hypothesis_generator import generate_hypotheses


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_json(filename, data):
    """Save data into a JSON file."""
    output_path = DATA_DIR / filename

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Saved: {output_path}")


def normalize_paper(paper, source):
    """Convert papers from different sources to a common format."""
    title = paper.get("title", "")
    abstract = paper.get("abstract") or paper.get("summary", "")

    normalized = dict(paper)
    normalized["source"] = source
    normalized["title"] = title
    normalized["abstract"] = abstract
    normalized["summary"] = abstract

    if not normalized.get("id"):
        normalized["id"] = (
            normalized.get("paper_id")
            or normalized.get("url")
            or title
        )

    return normalized


def literature_reviewer_agent(papers):
    print("\n[step 2] Reviewing research papers")

    reviewed_papers = []

    for paper in papers:
        try:
            reviewed = review_paper(paper)

            if isinstance(reviewed, dict):
                reviewed_papers.append(reviewed)
            else:
                reviewed_papers.append({
                    "title": paper.get("title", ""),
                    "source": paper.get("source", ""),
                    "review": str(reviewed),
                })

        except Exception as error:
            print(
                f"Review failed for "
                f"{paper.get('title', 'Unknown title')}: {error}"
            )

    save_json("reviewed_papers.json", reviewed_papers)
    return reviewed_papers


def hypothesis_generator_agent(reviewed_papers):
    print("\n[step 3] Generating hypotheses")

    hypotheses = generate_hypotheses(reviewed_papers)

    if not isinstance(hypotheses, list):
        hypotheses = [hypotheses]

    save_json("hypotheses.json", hypotheses)
    return hypotheses


def code_executor_agent(hypotheses):
    print("\n[step 4] Preparing experiment plans")

    experiment_plans = []

    for index, hypothesis in enumerate(hypotheses, start=1):
        if isinstance(hypothesis, dict):
            description = (
                hypothesis.get("hypothesis")
                or hypothesis.get("description")
                or hypothesis.get("title")
                or str(hypothesis)
            )
        else:
            description = str(hypothesis)

        experiment_plans.append({
            "experiment_id": index,
            "hypothesis": description,
            "execution_status": "not_executed",
            "note": "Plan prepared; generated code was not executed."
        })

    save_json("agent_experiment_plans.json", experiment_plans)

    print(
        f"Prepared {len(experiment_plans)} experiment plans. "
        "No generated code was executed."
    )

    return experiment_plans


def run_workflow():
    print("\n====================================")
    print(" AUTONOMOUS SCIENTIFIC DISCOVERY")
    print("====================================")

    print("\n[step 1] Fetching research papers")

    try:
        arxiv_papers = fetch_arxiv_papers(
            query="machine learning",
            max_results=5
        )

        pubmed_papers = fetch_pubmed_papers(
            query="machine learning",
            max_results=5
        )

    except Exception as error:
        print(f"Paper fetching failed: {error}")
        return

    arxiv_papers = [
        normalize_paper(paper, "arXiv")
        for paper in arxiv_papers
    ]

    pubmed_papers = [
        normalize_paper(paper, "PubMed")
        for paper in pubmed_papers
    ]

    papers = arxiv_papers + pubmed_papers

    print(f"arXiv papers fetched: {len(arxiv_papers)}")
    print(f"PubMed papers fetched: {len(pubmed_papers)}")
    print(f"Total papers collected: {len(papers)}")

    if not papers:
        print("No research papers were found.")
        return

    save_json("all_research_papers.json", papers)

    reviewed_papers = literature_reviewer_agent(papers)

    if not reviewed_papers:
        print("No papers could be reviewed.")
        return

    hypotheses = hypothesis_generator_agent(reviewed_papers)

    code_executor_agent(hypotheses)

    print("\n====================================")
    print(" WORKFLOW COMPLETED")
    print("====================================")
    print(f"Papers fetched: {len(papers)}")
    print(f"Papers reviewed: {len(reviewed_papers)}")
    print(f"Hypotheses generated: {len(hypotheses)}")
    print("Experiment plans prepared; no code was executed.")


if __name__ == "__main__":
    run_workflow()
