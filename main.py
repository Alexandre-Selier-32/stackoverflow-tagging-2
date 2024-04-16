from flask import Flask, request
import pickle
import csv
import re
from nltk.corpus import stopwords


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

@app.route("/bow_tags", methods=["POST"])
def bow__tags():

    def get_word_list():
        with open('word_list.csv') as f:
            read = csv.reader(f)
            nested_word_list = list(read)
            word_list = [row[0] for row in nested_word_list]
            return word_list

    def clean_and_split(sentence):

        def lower_keep_only_letters(sentence):
            for str_to_remove in [
                '<blockquote>',
                '</blockquote>',
                '<br>',
                '</br>',
                '<code>',
                '</code>',
                '<em>',
                '</em>',
                '<p>',
                '</p>',
                '<pre>',
                '</pre>',
                '<strong>',
                '</strong>'
            ]:
                sentence = sentence.replace(str_to_remove, ' ')

            sentence = sentence.lower()
            sentence = re.sub(r'[^a-z]', ' ', sentence)
            return sentence

        def remove_stop_words(split_words):
            split_words_without_stops = [word for word in split_words if word not in stopwords.words('english')]
            return split_words_without_stops

        sentence = lower_keep_only_letters(sentence)
        split_words = sentence.split()
        split_words_without_stops = remove_stop_words(split_words)
        return split_words_without_stops

    def get_presence_vector(tokens, word_list):
        presence_list = [1 if word in tokens else 0 for word in word_list]
        presence_vector = pd.Series(index=word_list, data=presence_list)
        return presence_vector

    question = request.form["question"]
    tokens = clean_and_split(question)
    word_list = get_word_list()
    presence_vector = get_presence_vector(tokens, word_list)
    bow_model = pickle.load(open("bow_model.sav", "rb"))
    tags = bow_model.predict([presence_vector])[0]
    return {"data": tags}



if __name__ == "__main__":
	app.run(debug=True)
