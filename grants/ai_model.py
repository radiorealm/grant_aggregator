from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def index_database(database):
    texts = [entry["text"] for entry in database]
    urls = [entry["url"] for entry in database]
    return texts, urls

def extract_keywords(query, top_n=5):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([query])
    scores = np.array(tfidf_matrix.sum(axis=0)).flatten()
    terms = np.array(vectorizer.get_feature_names_out())
    sorted_indices = np.argsort(scores)[::-1]
    top_keywords = terms[sorted_indices][:top_n]
    return top_keywords

def enhance_query_with_keywords(query, keywords, weight=2):
    words = query.split()
    enhanced_query = []
    for word in words:
        if word.lower() in keywords:
            enhanced_query.extend([word] * weight)
        else:
            enhanced_query.append(word)
    return " ".join(enhanced_query)

def find_most_similar(query_vector, vectors, top_n=3):
    similarities = cosine_similarity(query_vector, vectors)[0]
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    return top_indices, similarities[top_indices]

def handle_query(user_query, database, weight=2, top_keywords=5, top_n=10):
    if not database:
        return []
    texts, urls = index_database(database)
    vectors = model.encode(texts)
    keywords = extract_keywords(user_query, top_n=top_keywords)
    enhanced_query = enhance_query_with_keywords(user_query, keywords, weight)
    query_vector = model.encode([enhanced_query])
    top_indices, scores = find_most_similar(query_vector, vectors, top_n=top_n)
    return [
        {
            "URL": database[idx]['url'],
            "Текст": database[idx]['text'][:200] + "...",
            "Схожесть": f"{scores[i]:.2f}"
        }
        for i, idx in enumerate(top_indices)
    ]
