class StopLossEngine:
    """
    ATR-based stop loss and take profit engine.
    """

    @staticmethod
    def calculate_levels(
        entry_price: float,
        atr: float,
        risk_reward_ratio: float = 3.0
    ) -> dict:

        stop_loss = entry_price - atr

        risk = entry_price - stop_loss

        take_profit = (
            entry_price +
            (risk * risk_reward_ratio)
        )

        return {
            "entry_price": round(entry_price, 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "risk_reward_ratio": risk_reward_ratio
        }