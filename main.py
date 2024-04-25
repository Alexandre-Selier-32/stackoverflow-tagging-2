import nltk
import numpy as np
import pandas as pd
import pickle
import re
import sklearn

from flask import Flask, request

nltk.download("punkt")

app = Flask(__name__)

@app.route("/")
def index():
	return {"data": "Welcome to the StackOverflow tag predictor!"}

@app.route("/tags", methods=["POST"])
def tags():

    def predict_tags(title, body):

        def get_vectorized_title_and_body(title, body):

            def clean(document):

                TO_CONVERT = {
                    'c#': 'csharp',
                    'c++': 'cplusplus',
                    'asp.net': 'aspdotnet',
                    'node.js': 'nodejs'
                }

                def convert(string, to_convert=TO_CONVERT):
                    for key, value in to_convert.items():
                        string = string.replace(key, value)
                    return string

                TO_CONVERT_POST_TOKENIZATION = {'c': 'clanguage', 'r': 'rlanguage'}

                def convert_post_tokenization(tokens, to_convert_post_tokenization=TO_CONVERT_POST_TOKENIZATION):
                    for key, value in to_convert_post_tokenization.items():
                        for i, token in enumerate(tokens):
                            if token == key:
                                tokens[i] = value
                    return tokens

                HTML_TAGS = [
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
                ]

                def remove_html_tags(string, html_tags=HTML_TAGS):
                    for html_tag in html_tags:
                        string = string.replace(html_tag, ' ')
                    return string

                def keep_only_wanted_chars(string):
                    string = re.sub(r'[^a-zA-Z\.,:;?!\']', ' ', string)
                    return string

                document = document.lower()
                document = convert(document)
                document = remove_html_tags(document)
                document = keep_only_wanted_chars(document)
                document = nltk.tokenize.word_tokenize(document)
                document = convert_post_tokenization(document)
                document = ' '.join(document)
                return document

            def vectorize(vectorizer, document):

                vectorized_document = pd.DataFrame(
                    data=vectorizer.transform([document]).toarray(),
                    columns=vectorizer.get_feature_names_out()
                )

                return vectorized_document

            clean_title = clean(title)
            clean_body = clean(body)

            title_vectorizer = pickle.load(open('title_vectorizer.sav', 'rb'))

            vectorized_title = vectorize(title_vectorizer, clean_title)

            body_vectorizer = pickle.load(open('body_vectorizer.sav', 'rb'))

            vectorized_body = vectorize(body_vectorizer, clean_body)

            vectorized_title_and_body = pd.concat([vectorized_title, vectorized_body], axis=1)

            return vectorized_title_and_body

        def predict_tags_from_vectorized_title_and_body(vectorized_title_and_body):

            TAGS = [
                'javascript',
                'python',
                'java',
                'c_sharp',
                'php',
                'android',
                'html',
                'jquery',
                'c_plus_plus',
                'css',
                'ios',
                'sql',
                'mysql',
                'r',
                'reactjs',
                'node_js',
                'arrays',
                'c',
                'asp_net',
                'json'
            ]

            tag_predictor = pickle.load(open('tag_predictor.sav', 'rb'))

            pred_array = tag_predictor.predict(vectorized_title_and_body)[0]

            predicted_tags = []
            for i, tag in enumerate(TAGS):
                if pred_array[i] == 1:
                    predicted_tags.append(tag)

            return predicted_tags

        vectorized_title_and_body = get_vectorized_title_and_body(title, body)
        predicted_tags = predict_tags_from_vectorized_title_and_body(vectorized_title_and_body)
        return predicted_tags

    title = request.form["title"]
    body = request.form["body"]

    predicted_tags = predict_tags(title, body)

    return {"data": predicted_tags}


if __name__ == "__main__":
	app.run(debug=True)
