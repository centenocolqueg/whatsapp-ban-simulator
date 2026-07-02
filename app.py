from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Activo"

if __name__ == "__main__":
    # Esto arranca tu bot de Telegram en paralelo
    subprocess.Popen(["python", "bot.py"])
    # Esto arranca la web falsa que Render exige
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
