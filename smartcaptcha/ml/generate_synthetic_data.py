import random
import csv
import numpy as np

NUM_HUMANS = 500
NUM_BOTS = 300
OUTPUT_FILE = "synthetic_captcha_data.csv"

def generate_human():
    return {
        "avg_mouse_speed": round(float(np.random.uniform(0.3, 1.2)), 3),
        "mouse_path_entropy": round(float(np.random.uniform(0.25, 0.85)), 3),
        "click_delay": round(float(np.random.uniform(0.6, 2.5)), 3),
        "task_completion_time": round(float(np.random.uniform(2.0, 6.0)), 3),
        "idle_time": round(float(np.random.uniform(0.2, 1.5)), 3),
        "label": 1
    }

def generate_bot():
    return {
        "avg_mouse_speed": round(float(np.random.uniform(2.0, 4.0)), 3),
        "mouse_path_entropy": round(float(np.random.uniform(0.0, 0.08)), 3),
        "click_delay": round(float(np.random.uniform(0.01, 0.2)), 3),
        "task_completion_time": round(float(np.random.uniform(0.1, 0.8)), 3),
        "idle_time": round(float(np.random.uniform(0.0, 0.05)), 3),
        "label": 0
    }

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=generate_human().keys())
    writer.writeheader()
    for _ in range(NUM_HUMANS):
        writer.writerow(generate_human())
    for _ in range(NUM_BOTS):
        writer.writerow(generate_bot())

print("Synthetic data generated")
