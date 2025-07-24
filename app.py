from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/")
def index():
    return "Paytm Webhook Server Running!", 200

@app.route("/paytm-webhook", methods=["POST"])
def paytm_webhook():
    data = request.form.to_dict()
    print("Received Paytm data:", data)

    if data.get("STATUS") == "TXN_SUCCESS":
        message = (
            f"✅ *UPI Payment Received!*\n"
            f"Amount: ₹{data.get('TXNAMOUNT')}\n"
            f"Txn ID: `{data.get('TXNID')}`\n"
            f"Order ID: `{data.get('ORDERID')}`"
        )
    else:
        message = "⚠️ *Payment Failed or Invalid Format*\n" + str(data)

    # Send message to Telegram
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
    )

    return "OK", 200
