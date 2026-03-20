"""Neural Network model."""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


class ConflictPredictor(nn.Module):
    """Simple Neural Network for Conflict Prediction."""

    def __init__(self, input_size):
        super().__init__()
        self.layer1 = nn.Linear(input_size, 64)
        self.layer2 = nn.Linear(64, 32)
        self.output = nn.Linear(32, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.sigmoid(self.output(x))
        return x


def train_neural_network(X_train, y_train, X_test, y_test):
    """Train and evaluate Neural Network."""
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(
        y_train.values.reshape(-1, 1) if hasattr(y_train, "values") else y_train.reshape(-1, 1)
    )
    X_test_tensor = torch.FloatTensor(X_test)

    input_size = X_train.shape[1]
    model = ConflictPredictor(input_size)
    criterion = nn.BCELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)

    model.train()
    for _ in range(100):
        for data, target in train_loader:
            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, target)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        y_prob = test_outputs.numpy().flatten()
        y_pred = (y_prob > 0.5).astype(int)

    return {
        "model": model,
        "y_pred": y_pred,
        "y_prob": y_prob,
        "best_params": {"epochs": 100, "lr": 0.01},
        "name": "Neural Network",
    }
