import os

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

from analyzer import analyze_ingredients

app = Flask(__name__)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins == "*":
    CORS(app)
else:
    origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]
    CORS(app, resources={r"/*": {"origins": origins}})


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "NutriLabel backend is running"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    ingredient_text = data.get("ingredient_text", "")
    selected_profiles = data.get("selected_profiles", [])

    if not isinstance(ingredient_text, str):
        return jsonify({"error": "ingredient_text must be a string"}), 400

    if not isinstance(selected_profiles, list):
        return jsonify({"error": "selected_profiles must be a list"}), 400

    if not ingredient_text.strip():
        return jsonify({"error": "ingredient_text cannot be empty"}), 400

    result = analyze_ingredients(
        ingredient_text=ingredient_text,
        selected_profiles=selected_profiles,
        additives_tags=[],
        allergens_tags=[],
    )
    return jsonify(result)


@app.route("/product/<barcode>", methods=["GET"])
def get_product(barcode):
    selected_profiles = request.args.getlist("profile")

    off_url = (
        f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        f"?fields=product_name,product_name_en,ingredients_text,ingredients_text_en,brands,allergens_tags,additives_tags"
    )

    try:
        response = requests.get(
            off_url,
            timeout=20,
            headers={
                "User-Agent": "NutriLabel/1.0 (student project; contact: placeholder@example.com)"
            },
        )
        response.raise_for_status()
        off_data = response.json()
    except requests.RequestException as e:
        return jsonify({"error": "Could not reach Open Food Facts", "details": str(e)}), 502
    except ValueError as e:
        return jsonify({"error": "Invalid response from Open Food Facts", "details": str(e)}), 502

    if off_data.get("status") != 1:
        return jsonify({"error": "Product not found"}), 404

    product = off_data.get("product", {})
    ingredient_text = product.get("ingredients_text_en") or product.get("ingredients_text") or ""
    product_name = product.get("product_name_en") or product.get("product_name") or "Unknown Product"
    brands = product.get("brands", "")
    allergens = product.get("allergens_tags", []) or []
    additives = product.get("additives_tags", []) or []

    analysis = analyze_ingredients(
        ingredient_text=ingredient_text,
        selected_profiles=selected_profiles,
        additives_tags=additives,
        allergens_tags=allergens,
    )

    return jsonify({
        "barcode": barcode,
        "product_name": product_name,
        "brands": brands,
        "ingredient_text": ingredient_text,
        "allergens_tags": allergens,
        "additives_tags": additives,
        "analysis": analysis,
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
