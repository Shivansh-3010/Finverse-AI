from candlestick.pattern_detector import detect_doji
from candlestick.pattern_detector import detect_hammer
from candlestick.pattern_detector import detect_bullish_engulfing
from candlestick.pattern_detector import detect_bearish_engulfing
from candlestick.pattern_detector import detect_shooting_star
from candlestick.pattern_detector import detect_spinning_top


def test_doji():
    result = detect_doji(
        open_price=100,
        high_price=110,
        low_price=90,
        close_price=100.5,
    )

    print("Doji Detected:", result)
    
def test_hammer():
    result = detect_hammer(
        open_price=100,
        high_price=102,
        low_price=90,
        close_price=101,
    )

    print("Hammer Detected:", result)
    
def test_bullish_engulfing():
    result = detect_bullish_engulfing(
        prev_open=100,
        prev_close=95,
        curr_open=94,
        curr_close=102,
    )

    print("Bullish Engulfing Detected:", result)
    
def test_bearish_engulfing():
    result = detect_bearish_engulfing(
        prev_open=95,
        prev_close=100,
        curr_open=101,
        curr_close=94,
    )

    print("Bearish Engulfing Detected:", result)
    
def test_shooting_star():
    result = detect_shooting_star(
        open_price=100,
        high_price=112,
        low_price=99,
        close_price=101,
    )

    print("Shooting Star Detected:", result)
    
def test_spinning_top():
    result = detect_spinning_top(
        open_price=100,
        high_price=110,
        low_price=90,
        close_price=104,
    )

    print("Spinning Top Detected:", result)
    

if __name__ == "__main__":
    test_doji()
    test_hammer()
    test_bullish_engulfing()
    test_bearish_engulfing()
    test_shooting_star()
    test_spinning_top()