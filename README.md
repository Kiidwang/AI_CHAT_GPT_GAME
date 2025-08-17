# AI Chat GPT Game

This project contains a small Flask application that uses the OpenAI API to
host a text-based adventure game. The server generates the story and multiple
choice options via the API.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set the OpenAI API key:

   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

4. (Optional) Set a secret key for Flask sessions:

   ```bash
   export FLASK_SECRET_KEY="change_me"
   ```

## Running the server

Start the development server:

```bash
python app.py
```

Open a browser to `http://127.0.0.1:5000` and follow the prompts to play.
