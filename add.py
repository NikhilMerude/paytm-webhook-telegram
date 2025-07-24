from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route("/")
def home():
    return "Webhook is live"

@app.route("/paytm-webhook", methods=["POST"])
def paytm_webhook():
    data = request.form.to_dict()
    if data.get("STATUS") == "TXN_SUCCESS":
        msg = (
            f"💰 *UPI Payment Received!*\n"
            f"Amount: ₹{data.get('TXNAMOUNT')}\n"
            f"Txn ID: {data.get('TXNID')}\n"
            f"Order ID: {data.get('ORDERID')}\n"
            f"Mode: {data.get('PAYMENTMODE')}"
        )
    else:
        msg = "⚠️ Payment failed or unknown:\n" + str(data)

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    )
    return "OK", 200
