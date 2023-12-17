from flask import Flask, render_template, request, jsonify
import requests

RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
app = Flask(__name__)


@app.route("/message", methods=["POST"])
def webhook():
    try:
        user_message = request.get_json()["message"]
        print(f"User message: {user_message}")
    except KeyError:
        return jsonify({"message": "Invalid request format."}), 400

    rasa_response = requests.post(RASA_API_URL, json={"message": user_message})
    rasa_json = rasa_response.json()
    if not rasa_json:
        bot_message = "Sorry, I didn't get that. Please try again."
    else:
        bot_message = rasa_json[0].get("text", "Sorry, I didn't get that. Please try again.")

    print(f"Bot response: {bot_message}")
    return jsonify({"message": bot_message})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
