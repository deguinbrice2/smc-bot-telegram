import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Token lu depuis les variables d'environnement (jamais dans le code)
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data:
            return "No data", 400

        direction = data.get('signal', 'INCONNU')
        msg = (
            f"=== SMC/ICT SIGNAL ===\n"
            f"Direction : {direction}\n"
            f"Paire     : {data.get('pair', 'N/A')}\n"
            f"Timeframe : {data.get('tf', 'N/A')}\n"
            f"Entree    : {data.get('entry', 'N/A')}\n"
            f"Heure     : {data.get('time', 'N/A')}\n"
            f"====================="
        )

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": msg},
            timeout=10
        )
        return "OK", 200

    except Exception as e:
        print(f"Erreur : {e}")
        return "ERREUR", 500

@app.route('/', methods=['GET'])
def home():
    return "Bot SMC actif !", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
