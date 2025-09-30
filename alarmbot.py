import os
import requests
import time

# Telegram-Bot Daten aus Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# DexScreener API für deinen Token
API_URL = "https://api.dexscreener.com/token-pairs/v1/solana/UKbXwN3ySC2jP5p9TyQ91yXYXmnnDsjiZQ55QCqpump"

def send_alert(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload, timeout=10)
        print("✅ Benachrichtigung gesendet:", message)
    except Exception as e:
        print("❌ Fehler beim Senden:", e)

def check_token():
    try:
        r = requests.get(API_URL, timeout=10)
        data = r.json()

        # data ist eine Liste mit mindestens einem Pair
        if isinstance(data, list):
            pairs = data
        else:
            pairs = data.get("pairs", [])

        for pair in pairs:
            # Preisänderung in den letzten 24h
            change_24h = pair.get("priceChange", {}).get("h24")
            if change_24h is not None and float(change_24h) > 100:
                price = pair.get("priceUsd", "?")
                send_alert(
                    f"🚀 Token {pair['baseToken']['symbol']} hat in 24h +{change_24h:.1f}% erreicht! "
                    f"Aktueller Preis: ${price}"
                )

    except Exception as e:
        print("❌ Fehler bei API-Abfrage:", e)

if __name__ == "__main__":

    check_token()
