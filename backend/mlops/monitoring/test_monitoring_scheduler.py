from mlops.monitoring.monitoring_scheduler import (
    MonitoringScheduler,
)


def test():

    result = (
        MonitoringScheduler.run(
            model_name="xgboost",
            symbol="RELIANCE",
            timeframe="1d",
            horizon="5d",
        )
    )

    print(result)

    assert result["completed"] is True

    assert "report" in result

    assert "alerts" in result

    assert "recommendation" in result

    assert (
        result["report"]["model"]
        == "xgboost"
    )

    assert (
        "data_quality"
        in result["report"]
    )


if __name__ == "__main__":
    test()