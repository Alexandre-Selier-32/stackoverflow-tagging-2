from flask import Flask, request
import pickle

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

filename = "house_price_model.sav"
model = pickle.load(open(filename, "rb"))

@app.route("/house_price", methods=["POST"])
def house_price():
    area = int(request.form["area"])
    garden = int(request.form["garden"])
    price = model.predict([[area, garden]])[0]
    return {"data": price}

@app.route("/dummy_tags", methods=["POST"])
def dummy_tags():
    question = request.form["question"]
    return {"data": ["javascript", "python"]}

if __name__ == "__main__":
	app.run(debug=True)
