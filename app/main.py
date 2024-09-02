from fastapi import FastAPI, Query
from sklearn.feature_extraction.text import TfidfVectorizer

import os
import uvicorn
import numpy as np
import pandas as pd

def load_vectorizer():
    vectorizer = TfidfVectorizer()
    return vectorizer

def load_restaurants_reviews():
    current_dir = os.path.dirname(__file__)
    route = os.path.join(current_dir, "../data/trip_advisor_restaurants_sp.csv")

    restaurants_reviews = pd.read_csv(route)

    return restaurants_reviews

app = FastAPI()
app.vectorizer = load_vectorizer()
app.db = load_restaurants_reviews()

@app.get("/query")
def query_route(query: str = Query(..., description="Search query")):
    print(query)
    X = app.vectorizer.fit_transform(app.db['Description'])

    query_vector = app.vectorizer.transform([query])

    scores = np.array(X.dot(query_vector.T).todense()).flatten()

    app.db['Relevance Score'] = scores

    threshold = 0.01
    filtered_df = app.db[app.db['Relevance Score'] >= threshold]

    sorted_df = filtered_df.sort_values(by='Relevance Score', ascending=False)

    results = []
    for _, row in sorted_df.iterrows():
        results.append({
            'title': row['Name'],
            'content': row['Description'][:500],
            'relevance': row['Relevance Score']
        })

    return {"results": results, "message": "OK"}

def run():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run()