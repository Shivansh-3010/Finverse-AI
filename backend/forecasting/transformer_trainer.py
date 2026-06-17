import torch
import torch.nn as nn

from forecasting.transformer_engine import (
    TransformerEngine,
)


class TransformerTrainer:

    @staticmethod
    def train(
        X,
        y,
        epochs: int = 20,
        learning_rate: float = 0.001,
    ):

        model = TransformerEngine()

        criterion = nn.MSELoss()

        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=learning_rate,
        )

        X_tensor = torch.tensor(
            X,
            dtype=torch.float32,
        )

        y_tensor = torch.tensor(
            y,
            dtype=torch.float32,
        ).view(-1, 1)

        for epoch in range(
            epochs
        ):

            optimizer.zero_grad()

            predictions = model(
                X_tensor
            )

            loss = criterion(
                predictions,
                y_tensor
            )

            if epoch % 5 == 0:

                print(
                    f"Epoch {epoch}: {loss.item()}"
                )

            loss.backward()

            optimizer.step()

        return model