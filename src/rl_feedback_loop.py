import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RUNS_FILE = BASE_DIR / "data" / "experiment_runs.json"
FEEDBACK_FILE = BASE_DIR / "data" / "rl_feedback.json"

def evaluate_experiment(run):
    reward = 1 if run.get("status") == "success" else 0
    feedback = "Experiment successful" if reward else "Experiment needs improvement"
    return {"reward": reward, "feedback": feedback}

def run_feedback_loop():
    if not RUNS_FILE.exists():
        print(f"Runs file not found: {RUNS_FILE}")
        return

    with RUNS_FILE.open("r", encoding="utf-8") as file:
        runs = json.load(file)

    feedback_results = []

    for run in runs:
        evaluation = evaluate_experiment(run)
        feedback_results.append({
            "experiment_id": run.get("experiment_id", "UNKNOWN"),
            "reward": evaluation["reward"],
            "feedback": evaluation["feedback"],
            "evaluated_at": datetime.now(timezone.utc).isoformat()
        })

    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

    with FEEDBACK_FILE.open("w", encoding="utf-8") as file:
        json.dump(feedback_results, file, indent=4, ensure_ascii=False)

    print("RL Feedback Loop completed!")
    print(f"Experiments evaluated: {len(feedback_results)}")
    print(f"Feedback saved to: {FEEDBACK_FILE}")

if __name__ == "__main__":
    run_feedback_loop()
