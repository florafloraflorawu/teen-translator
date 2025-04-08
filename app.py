from flask import Flask, request, render_template
import openai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    translated = ""
    if request.method == 'POST':
        user_text = request.form['sentence']
        mode = request.form['mode']

        if mode == "to_teen":
            system_message = "You are a 12-year-old who rewrites sentences using Gen Alpha slang."
            prompt = f"Translate this sentence to how a teenager would say it: {user_text}"
        else:
            system_message = "You are a helpful adult who translates slang into regular English."
            prompt = f"Translate this teen slang into regular English: {user_text}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )

        translated = response.choices[0].message.content.strip()

    return render_template('index.html', translated=translated)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)




