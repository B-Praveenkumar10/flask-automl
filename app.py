from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# Azure ML Endpoint Details
AZURE_ENDPOINT = "https://praveenkumar-ml-zmish.eastus2.inference.ml.azure.com/score"
API_KEY = "EUqmtC0VLRqUYJidM7NCqKu7Dbe06YJOMqQ2ePklbGdNwoG0AwxgJQQJ99BCAAAAAAAAAAAAINFRAZML27vj"

# Headers for request
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    
    if request.method == 'POST':
        input_data = request.form.get("input_data", "{}")
        try:
            # Convert input to JSON
            payload = json.loads(input_data)
            
            # Send request to Azure ML Endpoint
            response = requests.post(AZURE_ENDPOINT, headers=HEADERS, json=payload)
            
            if response.status_code == 200:
                result = response.json()
            else:
                error = f"Request failed with status code {response.status_code}: {response.text}"
        except json.JSONDecodeError:
            error = "Invalid JSON input. Please enter valid JSON data."
    
    return render_template('index.html', result=result, error=error)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        payload = request.get_json()
        response = requests.post(AZURE_ENDPOINT, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Request failed with status code {response.status_code}", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": "Invalid request", "details": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
