import os
from flask import Flask
import threading
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "🟢 CENTRAL DE AUDITORÍA OPERATIVA ACTIVE"

def start_bot():
    # Arranca tu archivo bot.py en segundo plano
    subprocess.Popen(["python", "bot.py"])

if __name__ == "__main__":
    # Inicia el bot de Telegram en un hilo separado
    threading.Thread(target=start_bot, daemon=True).start()
    
    # IMPORTANTE: Forzamos a que escuche en el puerto 10000 (el que Render exige)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
