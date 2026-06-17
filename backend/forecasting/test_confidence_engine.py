from forecasting.confidence_engine import (
    ConfidenceEngine,
)


def test():

    confidence = (
        ConfidenceEngine.calculate(
            mae=0.4604,
            directional_accuracy=100.0,
        )
    )

    print(
        "Confidence:",
        confidence
    )


if __name__ == "__main__":
    test()