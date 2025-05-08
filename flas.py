from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis do .env (opcional, se quiser usar)
load_dotenv()

# Dados do Twilio – substitua por seus dados reais ou use .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "AC3c22ba1b64daf93f1c4ac090d93cc5b1")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "88b5445833b3e70215e606e1b0979ad1")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+19478377582")

app = Flask(__name__)

@app.route('/send', methods=['POST'])
def enviar_mensagem_whatsapp():
    data = request.get_json()

    numero = data.get("numero")
    mensagem = data.get("mensagem")

    if not numero or not mensagem:
        return jsonify({"erro": "Campos 'numero' e 'mensagem' são obrigatórios."}), 400

    try:
        response = requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            data={
                "From": f"whatsapp:{TWILIO_PHONE_NUMBER}",
                "To": f"whatsapp:{numero}",
                "Body": mensagem
            }
        )

        return jsonify({
            "status": "mensagem enviada",
            "twilio_status": response.status_code,
            "twilio_response": response.json()
        }), response.status_code

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7250)
