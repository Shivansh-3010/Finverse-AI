from risk.position_sizing_engine import PositionSizingEngine


def test_position_size():

    result = PositionSizingEngine.calculate_position_size(
        capital=100000,
        risk_percent=1,
        entry_price=100,
        stop_loss_price=95
    )

    assert result["quantity"] == 200
    assert result["max_risk_amount"] == 1000.0
    assert result["risk_per_share"] == 5.0


def test_zero_risk_per_share():

    result = PositionSizingEngine.calculate_position_size(
        capital=100000,
        risk_percent=1,
        entry_price=100,
        stop_loss_price=100
    )

    assert result["quantity"] == 0