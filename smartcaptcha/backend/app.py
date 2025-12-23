from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import joblib

model = joblib.load("captcha_model.pkl")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "SmartCAPTCHA backend alive"}


@app.post("/verify")
def verify(payload: dict):
    features = [[
        payload["avg_mouse_speed"],
        payload["mouse_path_entropy"],
        payload["click_delay"],
        payload["task_completion_time"],
        payload["idle_time"],
    ]]

    confidence = model.predict_proba(features)[0][1]

    human_like = (
        payload["avg_mouse_speed"] > 0.25 and
        payload["mouse_path_entropy"] > 0.15 and
        payload["click_delay"] > 0.4 and
        payload["task_completion_time"] > 1.2
    )

    decision = "human" if (human_like or confidence >= 0.4) else "bot"

    return {
        "decision": decision,
        "confidence": round(float(confidence), 3),
        "mode": "ml-assisted",
    }
