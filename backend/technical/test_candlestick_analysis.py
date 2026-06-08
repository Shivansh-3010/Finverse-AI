from technical.candlestick.candlestick_analysis import (
    analyze_candlestick,
)


def test_analysis():
    result = analyze_candlestick(
        open_price=100,
        high_price=112,
        low_price=99,
        close_price=101,
    )

    print(result)


if __name__ == "__main__":
    test_analysis()