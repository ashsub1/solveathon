from flask import Flask, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load trained model and scaler
model = joblib.load("pcos_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route("/", methods=["GET"])
def home():
    return "<h1 style='color:orange; text-align:center;'>PCOS Prediction App</h1>"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_data = np.array([[
            data["age"], data["weight"], data["height"], data["cycle_interval"],
            data["weight_gain"], data["hair_growth"], data["skin_darkening"],
            data["hair_loss"], data["acne"], data["fast_food"], data["exercise"],
            data["mood_swings"], data["regular_periods"], data["period_duration"]
        ]])

        # Scale input
        input_scaled = scaler.transform(input_data)

        # Predict probability
        prob_pcos = model.predict_proba(input_scaled)[:, 1][0]

        # Categorize probability
        if prob_pcos < 0.3:
            result = "No PCOS detected - Maintain a good lifestyle"
        elif prob_pcos < 0.7:
            result = "May have PCOS - Consider visiting a doctor"
        else:
            result = "High probability of PCOS - Must visit a doctor"

        return jsonify({"prediction": result, "probability": round(prob_pcos, 2)})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
