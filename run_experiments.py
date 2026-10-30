
import json
from pathlib import Path

from src.agents.agents.experiment_generator import generate_experiments

DATA_DIR = Path(__file__).resolve().parent / "data"


def main():
    input_file = DATA_DIR / "hypotheses.json"
    output_file = DATA_DIR / "experiments.json"

    if not input_file.exists():
        print("Error: hypotheses.json file nahi mili.")
        print("Pehle python main.py run karo.")
        return

    with input_file.open("r", encoding="utf-8") as file:
        hypotheses = json.load(file)

    if not isinstance(hypotheses, list):
        print("Error: hypotheses.json mein list honi chahiye.")
        return

    experiments = generate_experiments(hypotheses)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(experiments, file, indent=4, ensure_ascii=False)

    print(f"Successfully generated {len(experiments)} experiment plans.")
    print(f"Saved results to: {output_file}")


if __name__ == "__main__":
    main()
