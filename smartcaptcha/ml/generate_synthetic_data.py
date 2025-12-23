import random
import csv

NUM_HUMANS = 500
NUM_BOTS = 300
OUTPUT_FILE = "synthetic_captcha_data.csv"

def generate_human():
    return {
        "avg_mouse_speed": round(random.uniform(0.3, 1.5), 3),
        "mouse_path_entropy": round(random.uniform(0.2, 0.9), 3),
        "click_delay": round(random.uniform(0.5, 3.5), 3),
        "task_completion_time": round(random.uniform(1.5, 6.0), 3),
        "idle_time": round(random.uniform(0.0, 2.5), 3),
        "label": 1
    }

def generate_bot():
    return {
        "avg_mouse_speed": round(random.uniform(1.8, 4.0), 3),
        "mouse_path_entropy": round(random.uniform(0.0, 0.1), 3),
        "click_delay": round(random.uniform(0.0, 0.2), 3),
        "task_completion_time": round(random.uniform(0.2, 0.8), 3),
        "idle_time": 0.0,
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
