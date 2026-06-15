class PositionSizingEngine:
    """
    Risk-based position sizing.
    """

    @staticmethod
    def calculate_position_size(
        capital: float,
        risk_percent: float,
        entry_price: float,
        stop_loss_price: float
    ) -> dict:

        max_risk_amount = capital * (risk_percent / 100)

        risk_per_share = abs(
            entry_price - stop_loss_price
        )

        if risk_per_share == 0:
            return {
                "quantity": 0,
                "max_risk_amount": max_risk_amount
            }

        quantity = int(
            max_risk_amount / risk_per_share
        )

        return {
            "quantity": quantity,
            "max_risk_amount": round(max_risk_amount, 2),
            "risk_per_share": round(risk_per_share, 2)
        }