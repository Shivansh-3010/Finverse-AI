from feature_store.candlestick.candlestick_features import (
    generate_candlestick_features,
)


def test_candlestick_features():
    features = generate_candlestick_features(
        open_price=100,
        high_price=102,
        low_price=90,
        close_price=101,
    )

    print(features)


if __name__ == "__main__":
    test_candlestick_features()