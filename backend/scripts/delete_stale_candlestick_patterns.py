from database.session import SessionLocal
from sqlalchemy import text

AFFECTED_SYMBOLS = [
    'SBIN','ASIANPAINT','AXISBANK','BPCL','CIPLA',
    'DRREDDY','GRASIM','HDFC','HDFCBANK','HEROMOTOCO',
    'HINDALCO','HINDUNILVR','ICICIBANK','INFY','IOC',
    'ITC','MM','ONGC','RELIANCE','SUNPHARMA',
    'TATAMOTORS','TATASTEEL','TITAN','WIPRO','ZEEL',
    'BRITANNIA','VEDL','EICHERMOT','HCLTECH',
    'BAJFINANCE','GAIL','KOTAKBANK','INDUSINDBK',
    'SHREECEM','BHARTIARTL','MARUTI','UPL','LT',
    'ULTRACEMCO','TCS','NTPC','JSWSTEEL','TECHM',
    'POWERGRID','ADANIPORTS','BAJAJ-AUTO',
    'BAJAJFINSV','NESTLEIND','COALINDIA'
]

db = SessionLocal()

try:

    result = db.execute(
        text("""
        DELETE FROM candlestick_patterns
        WHERE symbol = ANY(:symbols)
        """),
        {"symbols": AFFECTED_SYMBOLS}
    )

    db.commit()

    print(
        f"Deleted: {result.rowcount:,}"
    )

finally:
    db.close()