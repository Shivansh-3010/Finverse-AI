from risk.stop_loss_engine import StopLossEngine


def test_stop_loss_levels():

    result = StopLossEngine.calculate_levels(
        entry_price=100,
        atr=5,
        risk_reward_ratio=3
    )

    assert result["stop_loss"] == 95
    assert result["take_profit"] == 115
    assert result["risk_reward_ratio"] == 3


def test_custom_risk_reward():

    result = StopLossEngine.calculate_levels(
        entry_price=100,
        atr=5,
        risk_reward_ratio=2
    )

    assert result["take_profit"] == 110