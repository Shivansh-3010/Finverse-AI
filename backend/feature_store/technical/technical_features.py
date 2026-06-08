import math

from technical.trend.sma import calculate_sma
from technical.trend.ema import calculate_ema
from technical.trend.adx import calculate_adx

from technical.momentum.rsi import calculate_rsi
from technical.momentum.macd import calculate_macd

from technical.volatility.atr import calculate_atr
from technical.volatility.bollinger_bands import calculate_bollinger_bands

from technical.volume.obv import calculate_obv
from technical.volume.vwap import calculate_vwap
from technical.volume.mfi import calculate_mfi


def generate_technical_features(data):
    """
    Generate technical features for ML models,
    recommendation engine,
    risk engine,
    and technical analysis agent.
    """

    # ADX fallback for small datasets
    try:
        adx = calculate_adx(data)
    except Exception:
        adx = {
            "adx": [0.0],
            "di_plus": [0.0],
            "di_minus": [0.0]
        }

    macd = calculate_macd(data)
    bb = calculate_bollinger_bands(data)

    latest_macd = float(macd["macd"].iloc[-1])
    latest_signal = float(macd["signal"].iloc[-1])

    if math.isnan(latest_macd):
        latest_macd = 0.0

    if math.isnan(latest_signal):
        latest_signal = 0.0

    return {
        "rsi": float(calculate_rsi(data).iloc[-1]),

        "sma_20": float(
            calculate_sma(data, 20).iloc[-1]
        ),

        "ema_20": float(
            calculate_ema(data, 20).iloc[-1]
        ),

        "atr": float(
            calculate_atr(data).iloc[-1]
        ),

        "adx": float(
            adx["adx"].iloc[-1]
            if hasattr(adx["adx"], "iloc")
            else adx["adx"][-1]
        ),

        "di_plus": float(
            adx["di_plus"].iloc[-1]
            if hasattr(adx["di_plus"], "iloc")
            else adx["di_plus"][-1]
        ),

        "di_minus": float(
            adx["di_minus"].iloc[-1]
            if hasattr(adx["di_minus"], "iloc")
            else adx["di_minus"][-1]
        ),

        "macd": latest_macd,
        "macd_signal": latest_signal,

        "obv": float(
            calculate_obv(data).iloc[-1]
        ),

        "vwap": float(
            calculate_vwap(data).iloc[-1]
        ),

        "mfi": float(
            calculate_mfi(data).iloc[-1]
        ),

        "bb_upper": float(
            bb["upper_band"].iloc[-1]
        ),

        "bb_middle": float(
            bb["middle_band"].iloc[-1]
        ),

        "bb_lower": float(
            bb["lower_band"].iloc[-1]
        ),
    }