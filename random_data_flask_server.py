from flask import Flask, jsonify
import random
import string

app = Flask(__name__)

@app.route('/')
def home():
    return (
        "Welcome to the Random Data API!\n"
        "Use the following endpoints to get random data:\n"
        "/random_number - Random number\n"
        "/random_string - Random string\n"
        "/random_quote  - Random quote\n"
        "/random_fact   - Random fact\n"
    )

@app.route('/random_number')
def random_number():
    number = random.randint(1, 100)
    return jsonify({"random_number": number})

@app.route('/random_string')
def random_string():
    length = 10
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return jsonify({"random_string": result_str})

@app.route('/random_quote')
def random_quote():
    quotes = [
        "Life is what happens when you're busy making other plans.",
        "The greatest glory in living lies not in never falling, but in rising every time we fall.",
        "The way to get started is to quit talking and begin doing.",
    ]
    quote = random.choice(quotes)
    return jsonify({"random_quote": quote})

@app.route('/random_fact')
def random_fact():
    facts = [
        "Honey never spoils.",
        "A single strand of spaghetti is called a 'spaghetto'.",
        "Bananas are berries, but strawberries aren't.",
    ]
    fact = random.choice(facts)
    return jsonify({"random_fact": fact})

if __name__ == '__main__':
    app.run(debug=True)
