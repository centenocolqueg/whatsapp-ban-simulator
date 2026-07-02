import os
import asyncio
from flask import Flask
import bot

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🟢 CENTRAL DE AUDITORÍA OPERATIVA - PROXYS ACTIVOS"

async def run_flask():
    # Ejecuta el servidor web obligatorio para Render de manera asíncrona
    config = flask_app.create_wsgi_app()
    port = int(os.environ.get("PORT", 5000))
    
    # Arranca un servidor local simplificado compatible con async
    from werkzeug.serving import make_server
    server = make_server("0.0.0.0", port, flask_app, threaded=True)
    print(f"Servidor Web iniciado en el puerto {port}")
    
    # Permite que el ciclo asíncrono no se bloquee
    while True:
        server.handle_request()
        await asyncio.sleep(0.5)

async def main():
    # Inicializa el bot de Telegram de forma segura
    telegram_app = bot.configurar_aplicacion()
    if not telegram_app:
        print("Error: No se configuró el token de Telegram.")
        return

    await telegram_app.initialize()
    await telegram_app.updater.start_polling()
    await telegram_app.start()
    print("Bucle de Telegram conectado con éxito.")

    # Ejecuta ambos servicios simultáneamente en el mismo bucle principal
    await asyncio.gather(
        run_flask(),
        asyncio.Event().wait()  # Mantiene el bucle corriendo indefinidamente
    )

if __name__ == "__main__":
    asyncio.run(main())
