
def generate_hypotheses(reviewed_papers, retrieved_context=""):
    """Generate preliminary, testable research hypotheses."""

    hypotheses = []
    context_text = str(retrieved_context or "").lower()

    for paper in reviewed_papers:
        if not isinstance(paper, dict):
            continue

        title = (
            paper.get("title")
            or paper.get("related_paper")
            or "Unknown topic"
        )
        review = (
            paper.get("review")
            or paper.get("evidence")
            or paper.get("summary")
            or paper.get("abstract")
            or ""
        )

        text = f"{title} {review}".lower()

        hypothesis = (
            f"Test whether an alternative method for '{title}' "
            "improves performance over the existing approach "
            "under controlled experimental conditions."
        )
        experiment = (
            "Compare the existing approach with a defined alternative "
            "using the same dataset and experimental setup."
        )
        metrics = ["task performance", "runtime"]
        research_area = "general"

        if any(word in text for word in [
            "surfel", "rendering", "reconstruction",
            "novel view", "radiance field", "hexagonal"
        ]):
            research_area = "3d_rendering"
            hypothesis = (
                "A compact surface representation may reduce memory "
                "usage while maintaining comparable rendering quality."
            )
            experiment = (
                "Compare a compact representation with a baseline "
                "on the same 3D scenes and rendering settings."
            )
            metrics = [
                "peak memory usage", "PSNR", "SSIM",
                "LPIPS", "rendering speed"
            ]

        elif any(word in text for word in [
            "robot", "robotic", "world model",
            "vision-language-action", "action-labeled"
        ]):
            research_area = "robotics"
            hypothesis = (
                "Training with imagined action outcomes may improve "
                "robot task success on previously unseen tasks."
            )
            experiment = (
                "Compare training with and without imagined action "
                "outcomes on held-out tasks."
            )
            metrics = [
                "task success rate",
                "generalization success rate",
                "failed trials"
            ]

        elif any(word in text for word in [
            "cosmos", "blockchain", "evm", "token transfer",
            "atomicity", "semantic-preserving"
        ]):
            research_area = "blockchain"
            hypothesis = (
                "Semantic validation and atomic transfer handling may "
                "reduce invalid or incomplete cross-chain transactions."
            )
            experiment = (
                "Test valid transfers, invalid transfers, and interrupted "
                "transactions against a baseline."
            )
            metrics = [
                "validation failure rate",
                "incomplete transaction rate",
                "transaction latency"
            ]

        elif any(word in text for word in [
            "test-time adaptation", "test time", "intervene",
            "normalization statistics", "distribution shift"
        ]):
            research_area = "test_time_adaptation"
            hypothesis = (
                "Selective test-time adaptation may improve robustness "
                "while reducing harmful model updates."
            )
            experiment = (
                "Compare selective adaptation with always-adapt and "
                "never-adapt baselines on clean and shifted data."
            )
            metrics = [
                "accuracy", "worst-group accuracy",
                "harmful intervention rate"
            ]

        elif any(word in text for word in [
            "prompt injection", "attention gates",
            "untrusted tokens", "instruction-data separation",
            "security defense"
        ]):
            research_area = "prompt_injection_security"
            hypothesis = (
                "Attention gates may reduce prompt-injection success "
                "while preserving performance on legitimate tasks."
            )
            experiment = (
                "Compare gated and ungated models on benign tasks and "
                "a controlled set of prompt-injection attacks."
            )
            metrics = [
                "attack success rate",
                "benign task accuracy",
                "false refusal rate"
            ]

        # Record whether retrieved context was available.
        # This does not mean the hypothesis has been scientifically validated.
        context_available = bool(context_text)

        hypotheses.append({
            "related_paper": title,
            "hypothesis": hypothesis,
            "evidence": review,
            "source": paper.get("link") or paper.get("source", ""),
            "research_area": research_area,
            "experiment": experiment,
            "evaluation_metrics": metrics,
            "retrieved_context_available": context_available,
            "status": "preliminary_not_validated"
        })

    return hypotheses
