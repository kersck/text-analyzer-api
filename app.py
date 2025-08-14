from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return """
    <h1>Text Analyzer API</h1>
    <p>Send POST request to /analyze with JSON: {"text": "your text here"}</p>
    <p>Example: curl -X POST -H "Content-Type: application/json" -d '{"text":"Hello world!"}' YOUR_URL/analyze</p>
    """

@app.route('/analyze', methods=['POST'])
def analyze_text():
    # Get JSON data from request
    data = request.get_json()
    
    # Check if text was provided
    if not data or 'text' not in data:
        return jsonify({"error": "Please provide 'text' in JSON body"}), 400
    
    text = data['text']
    
    # Perform analysis
    word_count = len(text.split())
    char_count = len(text)
    char_count_no_spaces = len(text.replace(' ', ''))
    sentence_count = len(re.split(r'[.!?]+', text)) - 1  # -1 because split creates empty string at end
    
    # Return results
    result = {
        "original_text": text,
        "analysis": {
            "word_count": word_count,
            "character_count": char_count,
            "character_count_no_spaces": char_count_no_spaces,
            "sentence_count": max(1, sentence_count)  # At least 1 sentence
        }
    }
    
    return jsonify(result)

if __name__ == '__main__':
    # Railway will provide PORT environment variable
    import os
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)
