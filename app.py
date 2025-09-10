from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import re
import os


app = Flask(__name__)
CORS(app)

# Load employee data
with open('employees.json', 'r') as f:
    data = json.load(f)

# Initialize embedding model
print("Loading embedding model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for all employees
def generate_embeddings():
    texts = []
    for emp in data['employees']:
        text = f"{emp['name']} {', '.join(emp['skills'])} {', '.join(emp['projects'])} {emp['experience_years']} years {emp['availability']}"
        texts.append(text)
    
    embeddings = embedding_model.encode(texts)
    return embeddings

# Create FAISS index
print("Creating vector index...")
employee_embeddings = generate_embeddings()
index = faiss.IndexFlatL2(employee_embeddings.shape[1])
index.add(employee_embeddings)

def find_employees(query):
    # Semantic search using embeddings
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(query_embedding, k=5)
    
    matches = []
    for i, idx in enumerate(indices[0]):
        if idx < len(data['employees']):
            emp = data['employees'][idx]
            
            # SIMPLE FIX: Ensure scores are always positive
            similarity_score = float(1 - distances[0][i])
            
            # Force positive scores
            if similarity_score < 0:
                similarity_score = 0.1  # Minimum positive value
            elif similarity_score > 1:
                similarity_score = 0.99  # Maximum cap
                
            matches.append({
                **emp, 
                'score': similarity_score,
                'match_reasons': [f"semantic similarity: {similarity_score:.2f}"]
            })
    
    # Also check for exact name matches (priority)
    query_lower = query.lower()
    for emp in data['employees']:
        if query_lower in emp['name'].lower():
            # Check if already in matches
            existing_match = next((m for m in matches if m['id'] == emp['id']), None)
            if existing_match:
                existing_match['score'] = 0.9
                existing_match['match_reasons'] = ["name match"]
            else:
                matches.append({
                    **emp,
                    'score': 0.9,
                    'match_reasons': ["name match"]
                })
    
    # Sort by score
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches

def generate_response(query, matches):
    if not matches:
        return "I couldn't find any employees matching your criteria. Try searching for specific skills like 'Python', 'React', or employee names."
    
    response = f"I found {len(matches)} potential candidates:\n\n"
    
    for i, emp in enumerate(matches[:3]):
        response += f"**{i+1}. {emp['name']}**\n"
        response += f"   - **Experience:** {emp['experience_years']} years\n"
        response += f"   - **Skills:** {', '.join(emp['skills'])}\n"
        response += f"   - **Projects:** {', '.join(emp['projects'])}\n"
        response += f"   - **Availability:** {emp['availability'].replace('_', ' ').title()}\n"
        response += f"   - **Match Reason:** {', '.join(emp['match_reasons'])}\n\n"
    
    return response

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    return app.response_class(
        response=json.dumps(data, indent=2, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

# Search employees
@app.route('/employees/search', methods=['GET'])
def search_employees():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    matches = find_employees(query)
    return jsonify({"query": query, "results": matches, "count": len(matches)})

# Chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')
        if not user_input:
            return jsonify({"error": "Message is required"}), 400
        
        matches = find_employees(user_input)
        response_text = generate_response(user_input, matches)
        
        return jsonify({
            "response": response_text, 
            "results": matches,
            "rag_system": True
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"HR Chatbot with RAG system starting on port {port}...")
    app.run(debug=True, host='0.0.0.0', port=port)