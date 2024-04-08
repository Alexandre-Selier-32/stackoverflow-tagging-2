from flask import Flask, request

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


if __name__ == "__main__":
	app.run(debug=True)
