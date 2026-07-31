import copy

import torch
import torch.nn as nn

from torch.utils.data import (
    DataLoader,
    TensorDataset,
    random_split,
)

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
        batch_size: int = 64,
        validation_split: float = 0.2,
    ):

        device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        input_size = X.shape[-1]

        model = TransformerEngine(
            input_size=input_size,
        ).to(device)

        criterion = nn.MSELoss()

        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=learning_rate,
            weight_decay=1e-4,
        )

        scheduler = (
            torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer,
                mode="min",
                factor=0.5,
                patience=5,
            )
        )

        X_tensor = torch.tensor(
            X,
            dtype=torch.float32,
        )

        y_tensor = torch.tensor(
            y,
            dtype=torch.float32,
        ).view(-1, 1)

        dataset = TensorDataset(
            X_tensor,
            y_tensor,
        )

        validation_size = max(
            1,
            int(
                len(dataset)
                * validation_split
            ),
        )

        train_size = (
            len(dataset)
            - validation_size
        )

        train_dataset, validation_dataset = random_split(
            dataset,
            [
                train_size,
                validation_size,
            ],
        )

        train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
        )

        validation_loader = DataLoader(
            validation_dataset,
            batch_size=batch_size,
            shuffle=False,
        )

        best_loss = float("inf")
        best_state = None

        patience = 10
        patience_counter = 0

        for epoch in range(epochs):

            model.train()

            train_loss = 0.0

            for batch_X, batch_y in train_loader:

                batch_X = batch_X.to(device)
                batch_y = batch_y.to(device)

                optimizer.zero_grad()

                predictions = model(batch_X)

                loss = criterion(
                    predictions,
                    batch_y,
                )

                loss.backward()

                torch.nn.utils.clip_grad_norm_(
                    model.parameters(),
                    1.0,
                )

                optimizer.step()

                train_loss += loss.item()

            train_loss /= len(train_loader)

            model.eval()

            validation_loss = 0.0

            with torch.no_grad():

                for batch_X, batch_y in validation_loader:

                    batch_X = batch_X.to(device)
                    batch_y = batch_y.to(device)

                    predictions = model(batch_X)

                    validation_loss += criterion(
                        predictions,
                        batch_y,
                    ).item()

            validation_loss /= len(validation_loader)

            scheduler.step(validation_loss)

            if validation_loss < best_loss:

                best_loss = validation_loss

                best_state = copy.deepcopy(
                    model.state_dict()
                )

                patience_counter = 0

            else:

                patience_counter += 1

            if epoch % 5 == 0:

                print(
                    f"Epoch {epoch} | "
                    f"Train={train_loss:.6f} | "
                    f"Val={validation_loss:.6f}"
                )

            if patience_counter >= patience:

                print(
                    f"Early stopping at epoch {epoch}"
                )

                break

        if best_state is not None:

            model.load_state_dict(
                best_state
            )

        return model