import os
from flask import Flask, request, render_template
import joblib
import pandas as pd

# -------------------------------------------------
# App initialization
# -------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------
# Load trained model pipeline
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_pipeline.pkl")

pipeline = joblib.load(MODEL_PATH)

# -------------------------------------------------
# Required input schema
# -------------------------------------------------
REQUIRED_COLUMNS = [
    "region",
    "crop",
    "season",
    "avg_temp_c",
    "total_rainfall_mm",
    "avg_humidity_pct",
    "drought_flag",
    "heat_stress_flag"
]

# -------------------------------------------------
# Home route (UI)
# -------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# -------------------------------------------------
# Prediction route (FORM BASED)
# -------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    form = request.form

    data = {
        "region": form["region"],
        "crop": form["crop"],
        "season": form["season"],
        "avg_temp_c": float(form["avg_temp_c"]),
        "total_rainfall_mm": float(form["total_rainfall_mm"]),
        "avg_humidity_pct": float(form["avg_humidity_pct"]),
        "drought_flag": int(form["drought_flag"]),
        "heat_stress_flag": int(form["heat_stress_flag"]),
    }

    df = pd.DataFrame([data])[REQUIRED_COLUMNS]

    # -------------------------------
    # MODEL PREDICTION (CLASS ONLY)
    # -------------------------------
    prediction = int(pipeline.predict(df)[0])

    # Convert class → interpretable probability
    if prediction == 1:
        prob = 0.7
        risk = "High"
    else:
        prob = 0.2
        risk = "Low"

    return render_template(
        "index.html",
        prediction=True,
        prob=round(prob, 2),
        risk=risk
    )

# -------------------------------------------------
# Run app
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
