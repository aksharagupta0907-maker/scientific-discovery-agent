
from pathlib import Path
from PIL import Image, ImageFilter
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
import numpy as np
import json
import time

# Project paths
ROOT = Path(__file__).resolve().parents[3]
DATASET = ROOT / "data" / "datasets" / "astronaut.png"
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

if not DATASET.exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET}")

# Load original image
image = Image.open(DATASET).convert("RGB")
original_array = np.array(image)

# Baseline timing
start = time.perf_counter()
baseline = image.copy()
baseline_time = time.perf_counter() - start

# Apply Gaussian blur
start = time.perf_counter()
processed = image.filter(ImageFilter.GaussianBlur(radius=1))
processed_time = time.perf_counter() - start

# Compare image quality
processed_array = np.array(processed)

psnr = peak_signal_noise_ratio(
    original_array, processed_array, data_range=255
)

ssim = structural_similarity(
    original_array,
    processed_array,
    channel_axis=2,
    data_range=255
)

# Save processed image
output_image = RESULTS / "astronaut_blurred.png"
processed.save(output_image)

# Create experiment report
report = {
    "experiment": "Lightweight image-processing prototype",
    "dataset": str(DATASET.relative_to(ROOT)),
    "image_dimensions": list(image.size),
    "baseline": "Original image (no processing)",
    "method": "Gaussian blur, radius 1",
    "evaluation": {
        "baseline_processing_time_seconds": baseline_time,
        "processed_time_seconds": processed_time,
        "psnr_db": float(psnr),
        "ssim": float(ssim),
        "output_file": str(output_image.relative_to(ROOT))
    },
    "status": "completed"
}

report_path = RESULTS / "image_experiment_report.json"
report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("Experiment completed successfully!")
print("Image dimensions:", image.size)
print(f"PSNR: {psnr:.2f} dB")
print(f"SSIM: {ssim:.4f}")
print("Processed image:", output_image)
print("Report saved:", report_path)
