from flask import Flask, request
import pickle
import csv


app = Flask(__name__)

@app.route("/")
def index():
	return {"data": "Homepage of GeeksForGeeks"}

@app.route("/hello", methods=["POST"])
def hello():
	return {"data": "Hello, Welcome to GeeksForGeeks lol"}

@app.route("/prod", methods=["POST"])
def prod():
    a = int(request.form["a"])
    b = int(request.form["b"])
    return {"data": a * b}

@app.route("/is_js", methods=["POST"])
def is_js():
    sentence = request.form["sentence"]
    result = "JavaScript" in sentence
    return {"data": result}

house_price_model = pickle.load(open("house_price_model.sav", "rb"))

@app.route("/house_price", methods=["POST"])
def house_price():
    area = int(request.form["area"])
    garden = int(request.form["garden"])
    price = house_price_model.predict([[area, garden]])[0]
    return {"data": price}

@app.route("/dummy_tags", methods=["POST"])
def dummy_tags():

    def get_word_list():
        with open('word_list.csv') as f:
            read = csv.reader(f)
            nested_word_list = list(read)
            word_list = [row[0] for row in nested_word_list]
            return word_list

    word_list = get_word_list()

    question = request.form["question"]
    return {"data": ["javascript", "python"]}



if __name__ == "__main__":
	app.run(debug=True)
