from training.trainers.universal_xgboost_trainer import (
    UniversalXGBoostTrainer,
)


def test_universal_trainer_smoke():

    UniversalXGBoostTrainer.train(
        horizon="1d",
        max_symbols=20,
    )

    assert True