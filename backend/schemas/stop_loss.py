from pydantic import BaseModel


class StopLossResponse(
    BaseModel
):
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward_ratio: float