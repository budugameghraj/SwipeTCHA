from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "captcha_model.pkl"

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    MODEL_LOADED = True
else:
    model = None
    MODEL_LOADED = False
    print("⚠️ ML model missing — running in safe fallback")


@app.get("/")
def root():
    return {"status": "backend alive"}


@app.post("/verify")
def verify(payload: dict):

    # ---------------------------
    # HARD BOT RULE (FIRST GATE)
    # ---------------------------
    # HARD BOT RULE (FINAL — SLIDER SAFE)
    if (
        payload["avg_mouse_speed"] > 3.0 and
        payload["mouse_path_entropy"] < 0.04 and
        payload["click_delay"] < 0.1 and
        payload["task_completion_time"] < 0.6
    ):
        return {
            "decision": "bot",
            "confidence": 0.0,
            "mode": "rule-blocked"
        }

    # ---------------------------
    # SAFE FALLBACK (NO MODEL)
    # ---------------------------
    if not MODEL_LOADED:
        return {
            "decision": "human",
            "confidence": 0.5,
            "mode": "fallback"
        }

    # ---------------------------
    # ML PREDICTION
    # ---------------------------
    features = [[
        payload["avg_mouse_speed"],
        payload["mouse_path_entropy"],
        payload["click_delay"],
        payload["task_completion_time"],
        payload["idle_time"]
    ]]

    confidence = float(model.predict_proba(features)[0][1])
    decision = "human" if confidence >= 0.65 else "bot"

    return {
        "decision": decision,
        "confidence": confidence,
        "mode": "ml-enabled"
    }
