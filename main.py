
import json
from pathlib import Path

from src.agents.agents.hypothesis_generator import generate_hypotheses

DATA_DIR = Path(__file__).resolve().parent / "data"


def main():
    input_file = DATA_DIR / "reviewed_papers.json"
    output_file = DATA_DIR / "hypotheses.json"

    if not input_file.exists():
        print("Error: reviewed_papers.json file nahi mili.")
        print("Pehle literature reviewer ko run karna hoga.")
        return

    with input_file.open("r", encoding="utf-8") as file:
        papers = json.load(file)

    if not isinstance(papers, list):
        print("Error: reviewed_papers.json mein list honi chahiye.")
        return

    hypotheses = generate_hypotheses(papers)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(hypotheses, file, indent=4, ensure_ascii=False)

    print(f"Successfully generated {len(hypotheses)} hypotheses.")
    print(f"Saved results to: {output_file}")

    for i, item in enumerate(hypotheses, start=1):
        print(f"\nHypothesis {i}:")
        print(item["hypothesis"])


if __name__ == "__main__":
    main()
