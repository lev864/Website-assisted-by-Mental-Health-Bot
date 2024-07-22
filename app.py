from groq import Groq
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import traceback 


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        client = Groq(
            api_key = 'API_KEY',
        )
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a mental health support chatbot. Answer the questions posed by an individual seeking mental support and advice empathetically and informatively"
                },
                {
                    "role": "user",
                    "content": f"{user_input}",
                }
            ],
            model="llama3-8b-8192",
        )
        message = response.choices[0].message.content
        return jsonify({"message": message})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
