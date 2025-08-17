import json
import os

from flask import Flask, render_template, request, session
import openai

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


def call_openai(messages):
    """Call the OpenAI API and return story text and options.

    The assistant is instructed to reply with JSON containing the keys
    ``story`` and ``options``. ``options`` should be a list of strings.
    """
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY is required to generate game content.")

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
    )
    content = response["choices"][0]["message"]["content"]

    try:
        data = json.loads(content)
        story = data.get("story", "")
        options = data.get("options", [])
    except json.JSONDecodeError:
        # If the model's response isn't valid JSON, return it as-is with no options.
        story = content
        options = []

    messages.append({"role": "assistant", "content": content})
    return story, options, messages


@app.route("/")
def index():
    """Start a new game."""
    # Initialize conversation with system prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are a text-based adventure game engine. "
                "After each player choice, describe the next part of the story "
                "and provide three numbered options for the player to choose from. "
                "Respond in JSON with keys 'story' and 'options'."
            ),
        }
    ]

    story, options, messages = call_openai(messages)
    session["messages"] = messages
    return render_template("game.html", story=story, options=options)


@app.route("/play", methods=["POST"])
def play():
    """Continue the game with the player's chosen option."""
    choice = request.form.get("option")
    messages = session.get("messages", [])
    messages.append({"role": "user", "content": choice})

    story, options, messages = call_openai(messages)
    session["messages"] = messages
    return render_template("game.html", story=story, options=options)


if __name__ == "__main__":
    app.run(debug=True)
