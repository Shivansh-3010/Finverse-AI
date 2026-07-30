from services.lstm_training_service import (
    LSTMTrainingService,
)


def test_import():

    assert (
        LSTMTrainingService
        is not None
    )