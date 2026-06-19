from forecasting.train_xgboost import (
    train,
)

from forecasting.horizons import (
    SUPPORTED_HORIZONS,
)


def train_all():

    print(
        "\n=== Multi-Horizon Training Started ===\n"
    )

    for horizon in SUPPORTED_HORIZONS:

        print(
            f"\nTraining Horizon: {horizon}\n"
        )

        try:

            train(
                horizon=horizon
            )

            print(
                f"\nSUCCESS: {horizon}\n"
            )

        except Exception as e:

            print(
                f"\nFAILED: {horizon}"
            )

            print(
                str(e)
            )

    print(
        "\n=== Multi-Horizon Training Finished ===\n"
    )


if __name__ == "__main__":

    train_all()