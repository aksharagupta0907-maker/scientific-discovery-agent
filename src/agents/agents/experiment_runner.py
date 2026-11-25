
import json
from pathlib import Path
from datetime import datetime, timezone


BASE_DIR = Path(__file__).resolve().parents[3]

INPUT_FILE = BASE_DIR / "data" / "agent_experiment_plans.json"
OUTPUT_FILE = BASE_DIR / "data" / "experiment_runs.json"


def prepare_experiments():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Experiment plans not found: {INPUT_FILE}"
        )

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        experiments = json.load(file)

    if not isinstance(experiments, list):
        raise ValueError("Experiment plans must contain a JSON list.")

    runs = []

    for experiment in experiments:
        runs.append({
            "experiment_id": experiment.get(
                "experiment_id", "UNKNOWN"
            ),
            "related_paper": experiment.get(
                "related_paper", ""
            ),
            "hypothesis": experiment.get("hypothesis", ""),
            "evaluation_metrics": experiment.get(
                "evaluation_metrics", []
            ),
            "status": "pending_execution",
            "prepared_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "result": None
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            runs,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Prepared {len(runs)} experiment runs.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    prepare_experiments()
