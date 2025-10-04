from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/clean', methods=['POST'])
def clean_data():
    if 'file' not in request.files or 'method' not in request.form:
        return jsonify({'error': 'Missing file or method'}), 400

    file = request.files['file']
    method = request.form['method']

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({'error': f'Error reading CSV: {str(e)}'}), 400

    if method == 'mean':
        cleaned_df = df.fillna(df.mean(numeric_only=True))
    elif method == 'median':
        cleaned_df = df.fillna(df.median(numeric_only=True))
    elif method == 'mode':
        mode_df = df.mode()
        if mode_df.empty:
            return jsonify({'error': 'No mode found for columns'}), 400
        cleaned_df = df.fillna(mode_df.iloc[0])
    else:
        return jsonify({'error': 'Invalid method'}), 400

    return cleaned_df.to_json(orient="records")

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)