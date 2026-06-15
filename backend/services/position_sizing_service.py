from risk.position_sizing_engine import (
    PositionSizingEngine,
)


class PositionSizingService:

    @staticmethod
    def calculate(
        capital: float,
        risk_percent: float,
        entry_price: float,
        stop_loss_price: float,
    ):

        return (
            PositionSizingEngine
            .calculate_position_size(
                capital=capital,
                risk_percent=risk_percent,
                entry_price=entry_price,
                stop_loss_price=stop_loss_price,
            )
        )