
import json
from pathlib import Path
from datetime import datetime, timezone


BASE_DIR = Path(__file__).resolve().parent.parent
RUNS_FILE = BASE_DIR / "data" / "experiment_runs.json"
FEEDBACK_FILE = BASE_DIR / "data" / "rl_feedback.json"


def evaluate_experiment(run):
    """
    Evaluate experiment execution and generate feedback.
    """

    status = run.get("status", "pending_execution")
    result = run.get("result")

    if status == "completed" and result is not None:
        return {
            "reward": 1,
            "feedback": "Experiment completed successfully."
        }

    if status == "failed":
        return {
            "reward": -1,
            "feedback": "Experiment failed. Review the error and improve the code."
        }

    return {
        "reward": 0,
        "feedback": "Experiment is pending. Execute it before evaluation."
    }


def run_feedback_loop():

    if not RUNS_FILE.exists():
        raise FileNotFoundError(
            f"Experiment runs file not found: {RUNS_FILE}"
        )

    with RUNS_FILE.open("r", encoding="utf-8") as file:
        runs = json.load(file)

    feedback_results = []

    for run in runs:

        evaluation = evaluate_experiment(run)

        feedback_results.append({
            "experiment_id": run.get("experiment_id", "UNKNOWN"),
            "reward": evaluation["reward"],
            "feedback": evaluation["feedback"],
            "evaluated_at": datetime.now(
                timezone.utc
            ).isoformat()
        })

    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

    with FEEDBACK_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            feedback_results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("RL Feedback Loop completed!")
    print(f"Experiments evaluated: {len(feedback_results)}")
    print(f"Feedback saved to: {FEEDBACK_FILE}")


if __name__ == "__main__":
    run_feedback_loop()
