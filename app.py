from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return render_template('chat.html')

    intent1 = request.form.get('intent1')
    intent2 = request.form.get('intent2')
    intent3 = request.form.get('intent3')

    # Verificar cuál no es None
    if intent1 is not None:
        intent=intent1
    elif intent2 is not None:
        intent=intent2
    elif intent3 is not None:
        intent=intent3

    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Eres un chatbot que recomienda películas, te llamas 'Next Moby'. Tu rol es responder recomendaciones de manera breve y concisa.",
                },
                {
                    "role": "user",
                    "content": "Recomiéndame una película de "+ intent,
                }
            ],
            model="gpt-4o",
            temperature=1
        )

    model_recommendation = chat_completion.choices[0].message.content
    return render_template('chat.html', recommendation=model_recommendation)


@app.route('/user/<username>')
def user(username):
    favorite_movies = [
        'The Shawshank Redemption',
        'The Godfather',
        'The Dark Knight',
    ]
    return render_template('user.html', username=username, favorite_movies=favorite_movies)


@app.post('/recommend')
def recommend():
    data = request.get_json()
    user_message = data['message']

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Eres un chatbot que recomienda películas, te llamas 'Next Moby'. Tu rol es responder recomendaciones de manera breve y concisa.",
            },
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model="gpt-4o",
    )

    message = chat_completion.choices[0].message.content

    return {
        'recommendation': message,
        'tokens': chat_completion.usage.total_tokens,
    }
