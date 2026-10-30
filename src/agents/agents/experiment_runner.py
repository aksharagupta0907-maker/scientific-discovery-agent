
import json
from pathlib import Path
from datetime import datetime, timezone

# Project ke main folder mein data directory
DATA_DIR = Path(__file__).resolve().parents[3] / "data"


def prepare_experiments():
    input_file = DATA_DIR / "experiments.json"
    output_file = DATA_DIR / "experiment_runs.json"

    if not input_file.exists():
        raise FileNotFoundError(
            f"Experiment plans not found: {input_file}"
        )

    with input_file.open("r", encoding="utf-8") as file:
        experiments = json.load(file)

    if not isinstance(experiments, list):
        raise ValueError("experiments.json must contain a JSON list.")

    runs = []

    for experiment in experiments:
        runs.append({
            "experiment_id": experiment.get("experiment_id", "UNKNOWN"),
            "related_paper": experiment.get("related_paper", ""),
            "hypothesis": experiment.get("hypothesis", ""),
            "evaluation_metrics": experiment.get(
                "evaluation_metrics", []
            ),
            "status": "pending_execution",
            "prepared_at": datetime.now(timezone.utc).isoformat(),
            "result": None
        })

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(runs, file, indent=4, ensure_ascii=False)

    print(f"Prepared {len(runs)} experiment runs.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    prepare_experiments()
