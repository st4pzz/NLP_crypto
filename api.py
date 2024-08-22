from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

app = Flask(__name__)

def remove_stop_words(stop_words, text):
    words = text.split()  # Divide o texto em palavras
    return ' '.join([word for word in words if word not in stop_words])

@app.route('/query', methods=['GET'])
def query():
    data = pd.read_csv("scraped_lyrics.csv")
    data = data.drop_duplicates(subset="Song Name", keep="first")
    data['Lyrics'] = data['Lyrics'].str.replace(r'[\r\n]+', ' ', regex=True).str.lower()

    

    # Alternativamente, você pode aplicar isso a todas as colunas de texto
   
    with open("stop_words.txt", "r") as file:
        stop_words = [line.strip() for line in file]

    data["Lyrics"] = data['Lyrics'].apply(lambda x: remove_stop_words(stop_words, x))
    
    
    query = request.args.get('query').lower()
    print(query)
    query = remove_stop_words(stop_words, query)
    print(query)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data["Lyrics"])
    Q = vectorizer.transform([query])
    R = X @ Q.T
    R = R.toarray().flatten()
    idx = R.argsort()[-10:][::-1]
    lista = []
    for i in idx:
        dici = {}
        dici['title'] = data.iloc[i]["Song Name"]
        dici['content'] = data.iloc[i]["Lyrics"]
        dici['relevance'] = R[i] 
        lista.append(dici)

    return jsonify({
        'results': lista,
        'message' : 'OK'
    })


if __name__ == "__main__":
    app.run(debug=True)