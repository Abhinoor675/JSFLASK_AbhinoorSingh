import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.compact = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(BASE_DIR, "dictionary.json")


def load_dictionary():
    if not os.path.exists(DICT_PATH):
        return {}
    with open(DICT_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_dictionary(data):
    with open(DICT_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


@app.route("/add", methods=["GET", "POST"])
def add_word():
    en_word = request.args.get("en")
    fi_word = request.args.get("fi")

    # Also support JSON body if tested with POST
    if not en_word or not fi_word:
        json_data = request.get_json(silent=True) or {}
        en_word = en_word or json_data.get("en")
        fi_word = fi_word or json_data.get("fi")

    if not en_word or not fi_word:
        return jsonify({"error": "Missing 'en' or 'fi' parameter"}), 400

    en_key = en_word.strip().lower()
    fi_val = fi_word.strip().lower()

    dictionary = load_dictionary()
    dictionary[en_key] = fi_val
    save_dictionary(dictionary)

    return jsonify({
        "message": "Word added successfully",
        "English": en_key,
        "Finnish": fi_val
    }), 201


@app.route("/translate/<word>", methods=["GET"])
def translate_word(word):
    dictionary = load_dictionary()
    key = word.lower()
    if key in dictionary:
        return jsonify({
            "English": key,
            "Finnish": dictionary[key]
        })
    return jsonify({"error": "Word not found"}), 404


@app.route("/words", methods=["GET"])
def list_words():
    dictionary = load_dictionary()
    return jsonify(list(dictionary.keys()))


if __name__ == "__main__":
    app.run(use_reloader=True, host="127.0.0.1", port=3000)