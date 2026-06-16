from agents.prediction_agent.agent import (
    PredictionAgent,
)


def test():

    result = (
        PredictionAgent.predict(
            symbol="RELIANCE",
            timeframe="1d"
        )
    )

    print(result)


if __name__ == "__main__":
    test()