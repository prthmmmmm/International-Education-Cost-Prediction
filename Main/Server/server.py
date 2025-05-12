from flask import Flask, request, jsonify, render_template
import torch
import torch.nn as nn
import pandas as pd
import joblib
from scipy.sparse import csr_matrix

app = Flask(__name__)

class CostPredictor(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)

    def forward(self, x):
        return self.fc3(torch.relu(self.fc2(torch.relu(self.fc1(x)))))

model = CostPredictor(789)
model.load_state_dict(torch.load("model_weights.pth"))
model.eval()
preprocessor = joblib.load("preprocessor.pkl")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = pd.DataFrame([request.get_json()])
        transformed_data = preprocessor.transform(input_data)

        if isinstance(transformed_data, csr_matrix):
            transformed_data = transformed_data.toarray()

        input_tensor = torch.tensor(transformed_data, dtype=torch.float32)
        prediction = model(input_tensor).item()

        return jsonify({'prediction': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
