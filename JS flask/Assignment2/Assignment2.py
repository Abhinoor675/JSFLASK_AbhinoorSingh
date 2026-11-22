import json
import os
from flask import Flask, jsonify

app = Flask(__name__)
app.json.compact = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(BASE_DIR, "dictionary.json")

with open(DICT_PATH, "r", encoding="utf-8") as file:
    dictionary = json.load(file)


@app.route("/translate/<word>", methods=["GET"])
def translate_word(word):
    key = word.lower()
    if key in dictionary:
        return jsonify({
            "English": key,
            "Finnish": dictionary[key]
        })
    return jsonify({"error": "Word not found"}), 404

@app.route("/words", methods=["GET"])
def list_words():
    return jsonify(list(dictionary.keys()))


if __name__ == "__main__":
    app.run(use_reloader=True, host="127.0.0.1", port=3000)