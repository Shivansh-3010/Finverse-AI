import math

import torch
import torch.nn as nn


class PositionalEncoding(nn.Module):

    def __init__(
        self,
        d_model: int,
        max_len: int = 5000,
    ):
        super().__init__()

        pe = torch.zeros(
            max_len,
            d_model,
        )

        position = torch.arange(
            0,
            max_len,
            dtype=torch.float32,
        ).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(
                0,
                d_model,
                2,
                dtype=torch.float32,
            )
            * (-math.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(
            position * div_term
        )

        pe[:, 1::2] = torch.cos(
            position * div_term
        )

        self.register_buffer(
            "pe",
            pe.unsqueeze(0),
        )

    def forward(self, x):

        return x + self.pe[:, : x.size(1)]


class TransformerEngine(nn.Module):

    def __init__(
        self,
        input_size: int,
        d_model: int = 64,
        nhead: int = 8,
        num_layers: int = 3,
        dropout: float = 0.2,
    ):
        super().__init__()

        self.embedding = nn.Linear(
            input_size,
            d_model,
        )

        self.position = PositionalEncoding(
            d_model
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dropout=dropout,
            batch_first=True,
            activation="gelu",
        )

        self.encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers,
        )

        self.norm = nn.LayerNorm(
            d_model
        )

        self.attention_pool = nn.Sequential(
            nn.Linear(
                d_model,
                1,
            )
        )

        self.dropout = nn.Dropout(
            dropout
        )

        self.head = nn.Sequential(
            nn.Linear(
                d_model,
                64,
            ),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(
                64,
                1,
            ),
        )

    def forward(
        self,
        x,
    ):

        x = self.embedding(x)

        x = self.position(x)

        x = self.encoder(x)

        x = self.norm(x)

        attention_weights = torch.softmax(
            self.attention_pool(x),
            dim=1,
        )

        x = torch.sum(
            attention_weights * x,
            dim=1,
        )

        x = self.dropout(x)

        return self.head(x)