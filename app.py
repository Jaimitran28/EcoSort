from flask import Flask, request, jsonify, render_template
import os
from fallback import fallback_classify

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict_image", methods=["POST"])
def predict_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]

    # Classify image using improved fallback_classify
    result = fallback_classify(file)

    return jsonify({
        "source": "image",
        "category": result["category"],
        "confidence": result["confidence"],
        "top_labels": result.get("top_labels", []),
        "tips": result.get("tips", [])
    })


@app.route("/predict_text", methods=["POST"])
def predict_text():
    from keywords import keyword_map, keyword_tips

    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text_input = data["text"].lower()

    category = "unknown"
    tips = ["Please describe a proper item."]

    # Find first matching keyword
    for keyword, cat in keyword_map.items():
        if keyword in text_input:
            category = cat
            tips = keyword_tips.get(keyword, ["No tips available."])
            break

    return jsonify({
        "source": "text",
        "category": category,
        "confidence": 1.0 if category != "unknown" else 0,
        "top_labels": [text_input] if category != "unknown" else [],
        "tips": tips
    })


if __name__ == "__main__":
    app.run(debug=True)
