
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[3]
INPUT_FILE = PROJECT_DIR / "data" / "experiments.json"
OUTPUT_FILE = PROJECT_DIR / "results" / "validation_report.json"


def validate_experiments():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        experiments = json.load(file)

    report = []

    for experiment in experiments:
        checks = {
            "has_experiment_id": bool(experiment.get("experiment_id")),
            "has_objective": bool(experiment.get("objective")),
            "has_design": bool(experiment.get("experiment_design")),
            "has_metrics": bool(experiment.get("evaluation_metrics")),
            "dataset_selected": (
                bool(experiment.get("dataset"))
                and experiment.get("dataset") != "To be selected and documented"
            ),
        }

        report.append({
            "experiment_id": experiment.get("experiment_id", "UNKNOWN"),
            "checks": checks,
            "ready_for_real_execution": all(checks.values()),
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    ready_count = sum(item["ready_for_real_execution"] for item in report)

    print(f"Experiments checked: {len(report)}")
    print(f"Ready for real execution: {ready_count}")
    print(f"Needs more setup: {len(report) - ready_count}")
    print(f"Report saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    validate_experiments()
