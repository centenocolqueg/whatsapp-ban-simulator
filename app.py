import os
import threading
from flask import Flask
import bot

app = Flask(__name__)

@app.route('/')
def home():
    return "🟢 CENTRAL DE AUDITORÍA OPERATIVA"

def run_bot():
    bot.main()

if __name__ == "__main__":
    # Inicia el bot en un hilo separado para que Flask no lo detenga
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Inicia el servidor Web que Render exige de forma gratuita
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
