import torch
import joblib
import numpy as np
import pandas as pd

def load_model(model_path):
    class CostPredictor(torch.nn.Module):
        def __init__(self, input_dim):
            super(CostPredictor, self).__init__()
            self.fc1 = torch.nn.Linear(input_dim, 128)
            self.fc2 = torch.nn.Linear(128, 64)
            self.fc3 = torch.nn.Linear(64, 1)

        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = torch.relu(self.fc2(x))
            x = self.fc3(x)
            return x

    model = CostPredictor(789)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def preprocess_input(data, preprocessor):
    df = pd.DataFrame([data])
    processed_input = preprocessor.transform(df)
    return processed_input
