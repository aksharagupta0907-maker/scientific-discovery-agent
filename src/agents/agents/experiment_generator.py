
def generate_experiments(hypotheses):
    """Convert hypotheses into structured experiment plans."""

    experiments = []

    for index, item in enumerate(hypotheses, start=1):
        title = item.get("related_paper", "Unknown paper")
        hypothesis = item.get("hypothesis", "")
        experiment = item.get(
            "experiment",
            "Compare a proposed approach against a baseline."
        )
        metrics = item.get("evaluation_metrics", ["task performance"])

        experiment_plan = {
            "experiment_id": f"EXP_{index:03d}",
            "related_paper": title,
            "hypothesis": hypothesis,
            "objective": (
                f"Evaluate the hypothesis associated with: {title}"
            ),
            "experiment_design": experiment,
            "baseline": "Existing or standard approach",
            "evaluation_metrics": metrics,
            "dataset": "To be selected and documented",
            "status": "planned_not_executed"
        }

        experiments.append(experiment_plan)

    return experiments
