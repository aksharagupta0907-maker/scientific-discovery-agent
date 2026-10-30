# Autonomous Multimodal Scientific Discovery Agent

## Project Overview
This project explores an automated scientific discovery workflow using Python. It includes literature review, hypothesis generation, experiment planning, validation, and a lightweight image-processing prototype.

## Technologies Used
- Python
- Pillow
- NumPy
- scikit-image
- JSON

## Current Experiment
- **Dataset:** Astronaut sample image
- **Image Size:** 512 × 512
- **Method:** Gaussian Blur (radius 1)
- **PSNR:** 29.66 dB
- **SSIM:** 0.9357
- **Status:** Completed

## Run the Experiment
Activate your virtual environment and run:

```bash
python src/agents/agents/image_experiment.py
```

## Output Files
- `results/astronaut_blurred.png`
- `results/image_experiment_report.json`
- `results/validation_report.json`

## Important Note
The image-processing experiment is a lightweight prototype for testing the workflow. It does not reproduce or validate the original Honeycomb-Surfels research paper.

## Future Improvements
- Improve literature retrieval and review.
- Generate evidence-based research hypotheses.
- Connect experiments to suitable scientific datasets.
- Add reproducible evaluation and result tracking.
