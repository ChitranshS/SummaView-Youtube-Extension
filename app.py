from flask import Flask, request, jsonify
from flask_cors import CORS
from transcript import main
from summarize_text import main_2
from comment_cat import commenter
from commentSentiment import commentSent
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/transcripted', methods=['POST']) # Handles Both Transcript and SRT
def transcripted():
    data = request.get_json()
    url = data.get('url')
    transcript = main(url)
    return jsonify(transcript)

@app.route('/summary', methods=['POST'])
def summary():
    data = request.get_json()
    url = data.get('url')
    transcript = main(url)
    summarized_text = main_2(transcript['text']) 
    return jsonify(summarized_text)

@app.route('/timestamp', methods=['POST']) # Handles Both Transcript and SRT
def timestamped():
    data = request.get_json()
    url = data.get('url')
    transcript = main(url)
    return jsonify(transcript)

@app.route('/commentcat', methods=['POST']) # Handles Both Transcript and SRT
def commentcat():
    data = request.get_json()
    url = data.get('url')
    comments = commenter(url)
    return jsonify(comments)

@app.route('/commentSentiment', methods=['POST']) # Handles Both Transcript and SRT
def commentS():
    data = request.get_json()
    url = data.get('url')
    comments = commentSent(url)
    return jsonify(comments)

if __name__ == '__main__':
    app.run(port=5000)