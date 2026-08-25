import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are FoodMate AI, a friendly food and restaurant assistant.

You can help users with:
- Food recommendations
- Restaurant suggestions
- Recipes
- Ingredients
- Cooking methods
- Healthy food choices
- Vegetarian and non-vegetarian food
- Breakfast, lunch and dinner ideas
- Food-related questions

Give simple, helpful and friendly answers.
If the user asks something unrelated to food, politely say that
you are FoodMate AI and mainly help with food and restaurant topics.
"""

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please enter a message."})

        prompt = SYSTEM_PROMPT + f"""

User: {user_message}

FoodMate AI:
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "reply": "Sorry, something went wrong. Please try again."
        })


if __name__ == "__main__":
    app.run(debug=True)