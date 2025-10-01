import os
import requests
import time
import datetime

# Telegram-Bot Daten aus Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ALERT_FILE = "last_alert.txt"

# DexScreener API für deinen Token
API_URL = "https://api.dexscreener.com/token-pairs/v1/solana/UKbXwN3ySC2jP5p9TyQ91yXYXmnnDsjiZQ55QCqpump"

def already_sent_today() -> bool:
  if not os.path.exists(ALERT_FILE):
        return False
    
  try:
    with open(ALERT_FILE, "r") as f:
      last_str = f.read().strip()
      last_time = datetime.fromisoformat(last_str)
      if datetime.utcnow() - last_time < timedelta(hours=24):
        return True
  except:
    return False
  return False

def set_alert_now():
    with open(ALERT_FILE, "w") as f:
        f.write(datetime.utcnow().isoformat()) 
        
def log_price(price, change_24h):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Preis: ${price}, Änderung: {change_24h}%")
    
def send_alert(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    if already_sent_today():
        return
    try:
        requests.post(url, json=payload, timeout=10)
        print("✅ Benachrichtigung gesendet:", message)
        set_alert_now()
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
            price = pair.get("priceUsd", "?")
            log_price(price,change_24h)
            if change_24h is not None and float(change_24h) > 1:
                send_alert(
                    f"🚀 Token {pair['baseToken']['symbol']} hat in 24h +{change_24h:.1f}% erreicht! "
                    f"Aktueller Preis: ${price}"
                )

    except Exception as e:
        print("❌ Fehler bei API-Abfrage:", e)

if __name__ == "__main__":

    check_token()












