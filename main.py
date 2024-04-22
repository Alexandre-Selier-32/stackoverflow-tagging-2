import csv
import numpy as np
import pandas as pd
import pickle
import re

from flask import Flask, request
from transformers import TFAutoModel


bert_model = TFAutoModel.from_pretrained('bert-base-uncased')

app = Flask(__name__)

@app.route("/")
def index():
	return {"data": "Welcome to the StackOverflow tag predictor!"}

@app.route("/bow_tags", methods=["POST"])
def bow__tags():

    def get_word_list():
        with open('word_list.csv') as f:
            read = csv.reader(f)
            nested_word_list = list(read)
            word_list = [row[0] for row in nested_word_list]
            return word_list

    def get_tag_list():
        with open('tag_list.csv') as f:
            read = csv.reader(f)
            nested_tag_list = list(read)
            tag_list = [row[0] for row in nested_tag_list]
            return tag_list

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
            stopwords = [
                'i',
                'me',
                'my',
                'myself',
                'we',
                'our',
                'ours',
                'ourselves',
                'you',
                "you're",
                "you've",
                "you'll",
                "you'd",
                'your',
                'yours',
                'yourself',
                'yourselves',
                'he',
                'him',
                'his',
                'himself',
                'she',
                "she's",
                'her',
                'hers',
                'herself',
                'it',
                "it's",
                'its',
                'itself',
                'they',
                'them',
                'their',
                'theirs',
                'themselves',
                'what',
                'which',
                'who',
                'whom',
                'this',
                'that',
                "that'll",
                'these',
                'those',
                'am',
                'is',
                'are',
                'was',
                'were',
                'be',
                'been',
                'being',
                'have',
                'has',
                'had',
                'having',
                'do',
                'does',
                'did',
                'doing',
                'a',
                'an',
                'the',
                'and',
                'but',
                'if',
                'or',
                'because',
                'as',
                'until',
                'while',
                'of',
                'at',
                'by',
                'for',
                'with',
                'about',
                'against',
                'between',
                'into',
                'through',
                'during',
                'before',
                'after',
                'above',
                'below',
                'to',
                'from',
                'up',
                'down',
                'in',
                'out',
                'on',
                'off',
                'over',
                'under',
                'again',
                'further',
                'then',
                'once',
                'here',
                'there',
                'when',
                'where',
                'why',
                'how',
                'all',
                'any',
                'both',
                'each',
                'few',
                'more',
                'most',
                'other',
                'some',
                'such',
                'no',
                'nor',
                'not',
                'only',
                'own',
                'same',
                'so',
                'than',
                'too',
                'very',
                's',
                't',
                'can',
                'will',
                'just',
                'don',
                "don't",
                'should',
                "should've",
                'now',
                'd',
                'll',
                'm',
                'o',
                're',
                've',
                'y',
                'ain',
                'aren',
                "aren't",
                'couldn',
                "couldn't",
                'didn',
                "didn't",
                'doesn',
                "doesn't",
                'hadn',
                "hadn't",
                'hasn',
                "hasn't",
                'haven',
                "haven't",
                'isn',
                "isn't",
                'ma',
                'mightn',
                "mightn't",
                'mustn',
                "mustn't",
                'needn',
                "needn't",
                'shan',
                "shan't",
                'shouldn',
                "shouldn't",
                'wasn',
                "wasn't",
                'weren',
                "weren't",
                'won',
                "won't",
                'wouldn',
                "wouldn't"]
            split_words_without_stops = [word for word in split_words if word not in stopwords]
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
    tag_recommendation_bools = bow_model.predict([presence_vector])[0].tolist()
    tag_list = get_tag_list()

    recommended_tags = []
    for i, tag in enumerate(tag_list):
        if tag_recommendation_bools[i] == 1:
            recommended_tags.append(tag)

    return {"data": recommended_tags}


if __name__ == "__main__":
	app.run(debug=True)
