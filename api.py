from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

app = Flask(__name__)

@app.route('/query', methods=['GET'])
def query():
    data = pd.read_csv("./hate_speech/HateSpeechDataset.csv")
    query = request.args.get('query')
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data["Content"])
    Q = vectorizer.transform(query)
    R = X @ Q.T
    R = R.toarray().flatten()
    idx = R.argsort()[-10:]
    lista = []
    for i in idx:
        dici = {}
        
        dici['content'] = data.iloc[i]["Content"]
        dici['relevance'] = idx[i]
        lista.append(dici)

    return jsonify({
        'results': lista,
        'message' : 'OK'
    })


if __name__ == "__main__":
    app.run(debug=True)