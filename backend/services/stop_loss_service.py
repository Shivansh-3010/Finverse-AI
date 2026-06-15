from risk.stop_loss_engine import (
    StopLossEngine,
)


class StopLossService:

    @staticmethod
    def calculate(
        entry_price: float,
        atr: float,
        risk_reward_ratio: float = 3.0,
    ):

        return (
            StopLossEngine.calculate_levels(
                entry_price=entry_price,
                atr=atr,
                risk_reward_ratio=risk_reward_ratio,
            )
        )