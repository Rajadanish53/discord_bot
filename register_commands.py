"""
One-time script to register slash commands with Discord.
Run locally: set DISCORD_TOKEN and DISCORD_APP_ID, then: python register_commands.py
"""
import os
import requests

DISCORD_API = "https://discord.com/api/v10"
TOKEN = os.environ.get("DISCORD_TOKEN", "").strip()
APP_ID = os.environ.get("DISCORD_APP_ID", "").strip()

COMMANDS = [
    {
        "name": "lot",
        "description": "Calculate lot size for any trading pair",
        "options": [
            {"name": "acc_size", "description": "Your account size in USD", "type": 10, "required": True},
            {"name": "risk", "description": "Risk percentage (1-5% recommended)", "type": 10, "required": True},
            {"name": "pair", "description": "Trading pair (XAUUSD, EURUSD, US100, etc.)", "type": 3, "required": True},
            {"name": "sl", "description": "Stop loss in pips", "type": 10, "required": True},
        ],
    },
    {"name": "pairs", "description": "Show all supported trading pairs", "options": []},
    {"name": "quick", "description": "Quick lot size examples", "options": []},
]


def main():
    if not TOKEN or not APP_ID:
        print("Set DISCORD_TOKEN and DISCORD_APP_ID environment variables.")
        return
    url = f"{DISCORD_API}/applications/{APP_ID}/commands"
    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}
    r = requests.put(url, json=COMMANDS, headers=headers)
    if r.status_code == 200:
        print("Slash commands registered successfully.")
    else:
        print(f"Error {r.status_code}: {r.text}")


if __name__ == "__main__":
    main()
