
def generate_hypotheses(reviewed_papers):
    """Generate preliminary, testable research hypotheses from paper reviews."""

    hypotheses = []

    for paper in reviewed_papers:
        title = paper.get("title") or paper.get("related_paper") or "Unknown topic"
        review = paper.get("review") or paper.get("evidence") or ""
        text = f"{title} {review}".lower()

        # Default hypothesis if no specific research area matches.
        hypothesis = (
            f"Test whether an alternative method for '{title}' "
            "improves performance over the existing approach "
            "under controlled experimental conditions."
        )
        experiment = (
            "Compare the existing approach with a clearly defined "
            "alternative using the same dataset and experimental setup."
        )
        metrics = ["task performance", "runtime"]
        research_area = "general"

        if any(word in text for word in [
            "surfel", "rendering", "reconstruction",
            "novel view", "radiance field", "hexagonal"
        ]):
            research_area = "3d_rendering"
            hypothesis = (
                "A compact surface representation can reduce memory "
                "usage while maintaining comparable novel-view "
                "rendering quality."
            )
            experiment = (
                "Compare the compact representation with a baseline "
                "on the same 3D scenes and rendering settings."
            )
            metrics = [
                "peak memory usage",
                "PSNR",
                "SSIM",
                "LPIPS",
                "rendering speed"
            ]

        elif any(word in text for word in [
            "thinkworld", "robotic", "robot", "world model",
            "vision-language-action", "action-labeled"
        ]):
            research_area = "robotics"
            hypothesis = (
                "Training with imagined action outcomes alongside "
                "available demonstrations may improve robot task "
                "success on previously unseen objects or environments."
            )
            experiment = (
                "Compare training with and without imagined action "
                "outcomes on held-out tasks, using the same evaluation "
                "conditions."
            )
            metrics = [
                "task success rate",
                "generalization success rate",
                "number of failed trials"
            ]

        elif any(word in text for word in [
            "cosmos", "blockchain", "evm", "token transfer",
            "atomicity", "semantic-preserving"
        ]):
            research_area = "blockchain"
            hypothesis = (
                "Explicit semantic validation combined with atomic "
                "transfer handling may reduce invalid token transfers "
                "and incomplete transactions across heterogeneous chains."
            )
            experiment = (
                "Test valid and invalid transfers, injected failures, "
                "and interrupted transactions against a baseline bridge."
            )
            metrics = [
                "semantic validation failure rate",
                "incomplete transaction rate",
                "transaction latency",
                "recovery success rate"
            ]

        elif any(word in text for word in [
            "test-time adaptation", "test time", "intervene",
            "normalization statistics", "distribution shift"
        ]):
            research_area = "test_time_adaptation"
            hypothesis = (
                "A selective test-time intervention policy based on "
                "input uncertainty or distribution shift may improve "
                "robustness while reducing harmful model updates."
            )
            experiment = (
                "Compare selective intervention with always-adapt "
                "and never-adapt baselines across clean and corrupted "
                "evaluation batches."
            )
            metrics = [
                "accuracy",
                "worst-group accuracy",
                "harmful intervention rate",
                "performance on clean data"
            ]

        elif any(word in text for word in [
            "prompt injection", "attention gates",
            "untrusted tokens", "instruction-data separation",
            "security defense"
        ]):
            research_area = "prompt_injection_security"
            hypothesis = (
                "Learned attention gates may reduce prompt-injection "
                "attack success while preserving performance on "
                "legitimate tasks."
            )
            experiment = (
                "Compare the gated model with an ungated baseline "
                "on benign tasks and a controlled set of prompt-injection "
                "attacks."
            )
            metrics = [
                "attack success rate",
                "benign task accuracy",
                "false refusal rate",
                "utility retention"
            ]

        hypotheses.append({
            "related_paper": title,
            "hypothesis": hypothesis,
            "evidence": review,
            "source": paper.get("link") or paper.get("source", ""),
            "research_area": research_area,
            "experiment": experiment,
            "evaluation_metrics": metrics,
            "status": "preliminary_not_validated"
        })

    return hypotheses
