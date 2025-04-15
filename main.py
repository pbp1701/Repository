from flask import Flask, request, jsonify
from datetime import datetime
import os, json

app = Flask(__name__)

NOTES_FILE = 'notes.json'

if os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, 'r') as f:
        notes = json.load(f)
else:
    notes = []

@app.route('/')
def home():
    return 'API is live!'

@app.route('/note', methods=['POST'])
def store_note():
    data = request.get_json()
    note_text = data.get('note')
    category = data.get('category', 'Uncategorized')
    tags = data.get('tags', [])
    timestamp = data.get('timestamp', datetime.utcnow().isoformat())

    if not note_text:
        return jsonify({'error': 'Missing note text'}), 400

    note_entry = {
        'id': f'note_{len(notes)+1}',
        'note': note_text,
        'category': category,
        'tags': tags,
        'timestamp': timestamp
    }

    notes.append(note_entry)
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)

    return jsonify({'status': 'saved', 'id': note_entry['id']})

@app.route('/notes', methods=['GET'])
def get_notes():
    return jsonify(notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
