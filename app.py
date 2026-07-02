import os
import threading
from flask import Flask
import bot  # Importa directamente las funciones de tu bot.py

app = Flask(__name__)

@app.route('/')
def home():
    # Página web obligatoria para mantener Render activo
    return "🟢 CENTRAL DE AUDITORÍA OPERATIVA - INTERFAZ EN LÍNEA"

def iniciar_bot_telegram():
    # Ejecuta el bucle principal del bot dentro del mismo proceso
    print("Iniciando bucle de Telegram...")
    bot.main()

if __name__ == "__main__":
    # Arranca el bot en un hilo nativo del mismo proceso antes de abrir la web
    t = threading.Thread(target=iniciar_bot_telegram)
    t.daemon = True
    t.start()
    
    # Arranca el servidor web en el puerto asignado por Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
