"""Shared lot size calculator logic (used by bot and serverless)."""
import datetime


def calculate_lot_size(account_balance, risk_percent, stop_loss_pips, instrument):
    """Calculate lot size based on instrument type."""
    risk_amount = account_balance * (risk_percent / 100)

    pip_values = {
        'EURUSD': 10.0, 'GBPUSD': 10.0, 'USDJPY': 9.0, 'USDCHF': 10.0,
        'AUDUSD': 10.0, 'USDCAD': 10.0, 'NZDUSD': 10.0,
        'EURGBP': 10.0, 'EURJPY': 10.0, 'GBPJPY': 10.0,
        'AUDJPY': 10.0, 'CADJPY': 9.0, 'CHFJPY': 9.0,
        'XAUUSD': 10.0, 'GOLD': 10.0, 'XAGUSD': 5.0, 'SILVER': 5.0,
        'US30': 1.0, 'US100': 2.0, 'SPX500': 0.5, 'NAS100': 2.0, 'DOW': 1.0,
        'USOIL': 10.0, 'UKOIL': 10.0, 'OIL': 10.0, 'XTIUSD': 10.0,
        'BTCUSD': 1.0, 'ETHUSD': 1.0, 'XRPUSD': 1.0, 'LTCUSD': 1.0,
    }

    pip_value = pip_values.get(instrument.upper(), 10.0)
    lot_size = risk_amount / (stop_loss_pips * pip_value)
    if lot_size < 0.01:
        lot_size = 0.01

    return round(lot_size, 2), risk_amount, pip_value


def build_lot_embed(acc_size, risk, pair, sl, lot_size, risk_amount):
    """Build Discord embed dict for /lot response."""
    current_time = datetime.datetime.utcnow().strftime("%m/%d/%y, %I:%M %p").replace(" 0", " ").lstrip("0")
    return {
        "title": "CULT TRADERS CALCULATOR APP",
        "description": current_time,
        "color": 0x00ff00,
        "fields": [
            {"name": "**LOT SIZE CALCULATOR**", "value": "\u200b", "inline": False},
            {"name": "ACCOUNT SIZE", "value": f"${acc_size:,.1f}", "inline": False},
            {"name": "RISK", "value": f"{risk}% = ${risk_amount:.1f}", "inline": False},
            {"name": "PAIR", "value": pair.upper(), "inline": False},
            {"name": "STOP-LOSS", "value": f"{sl} pips", "inline": False},
            {"name": "CALCULATED LOT SIZE", "value": f"**{lot_size:.2f}**", "inline": False},
        ],
        "footer": {"text": "BY CULT TRADERS"},
    }


def build_pairs_embed():
    """Build Discord embed dict for /pairs response."""
    return {
        "title": "SUPPORTED TRADING PAIRS",
        "color": 0x0099ff,
        "fields": [
            {"name": "MAJOR FOREX", "value": "EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD", "inline": False},
            {"name": "CROSS PAIRS", "value": "EURGBP, EURJPY, GBPJPY, AUDJPY, CADJPY, CHFJPY", "inline": False},
            {"name": "METALS", "value": "XAUUSD (Gold), XAGUSD (Silver)", "inline": False},
            {"name": "INDICES", "value": "US30 (Dow Jones), US100 (NASDAQ), SPX500 (S&P 500)", "inline": False},
            {"name": "COMMODITIES", "value": "USOIL, UKOIL", "inline": False},
            {"name": "CRYPTO", "value": "BTCUSD, ETHUSD, XRPUSD, LTCUSD", "inline": False},
            {"name": "USAGE", "value": "Use `/lot acc_size:1000 risk:2 pair:XAUUSD sl:50`", "inline": False},
        ],
    }


def build_quick_embed():
    """Build Discord embed dict for /quick response."""
    return {
        "title": "QUICK EXAMPLES",
        "color": 0xffa500,
        "fields": [
            {"name": "Example 1:", "value": "`/lot acc_size:1000 risk:2 pair:XAUUSD sl:50`\n• ACCOUNT SIZE: $1,000.0\n• RISK: 2.0% = $20.0\n• PAIR: XAUUSD\n• STOP-LOSS: 50 pips\n• CALCULATED LOT SIZE: **0.04**", "inline": False},
            {"name": "Example 2:", "value": "`/lot acc_size:5000 risk:1 pair:EURUSD sl:30`\n• ACCOUNT SIZE: $5,000.0\n• RISK: 1.0% = $50.0\n• PAIR: EURUSD\n• STOP-LOSS: 30 pips\n• CALCULATED LOT SIZE: **0.17**", "inline": False},
            {"name": "Risk Management", "value": "Maximum Risk Limit: **20%**\nRecommended: 1-2% risk per trade", "inline": False},
        ],
    }
