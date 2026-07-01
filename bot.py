import os
import random
import time
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Simulador de WhatsApp Mod/Ban Activo**\n\n"
        "Este es un bot de entretenimiento para simular interacciones de auditoría ficticias.\n\n"
        "📌 **Comandos disponibles:**\n"
        "🔹 `/ban <número>` - Simular reporte masivo\n"
        "🔹 `/unban <número>` - Simular petición de desbloqueo\n"
        "🔹 `/check <número>` - Simular escaneo de seguridad\n"
        "🔹 `/ayuda` - Ver advertencia legal e información"
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚠️ **DESCARGO DE RESPONSABILIDAD LEGAL** ⚠️\n\n"
        "Este bot es estrictamente un **simulador educativo y de bromas**.\n"
        "• Ninguna acción realizada aquí afecta a cuentas reales de WhatsApp.\n"
        "• No realiza ataques informáticos, denegación de servicio (DoS) ni spam real.\n"
        "• Modificar o suspender cuentas ajenas sin autorización viola los términos de Meta y las leyes locales de ciberseguridad."
    )

async def ban_simulator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Uso correcto: `/ban +51999888777`")
        return
    
    target_number = " ".join(context.args)
    msg = await update.message.reply_text(f"🔍 Conectando con nodos de reporte simulados para {target_number}...")
    await asyncio.sleep(2)
    await msg.edit_text("🛰️ Generando firmas de Spam artificiales (1/3)...")
    await asyncio.sleep(2)
    await msg.edit_text("⚙️ Enviando 500 reportes simulados a la cola de revisión (2/3)...")
    await asyncio.sleep(2)
    await msg.edit_text("⚡ Forzando desconexión del token de sesión ficticio (3/3)...")
    await asyncio.sleep(1.5)
    
    final_status = random.choice([
        f"⚠️ **SIMULACIÓN EXITOSA** ⚠️\n\nEl sistema automatizado ficticio reporta que el número {target_number} ha entrado en revisión de términos.",
        f"❌ **SIMULACIÓN FALLIDA**\n\nEl número {target_number} posee protección simulada contra reportes masivos."
    ])
    await msg.edit_text(final_status)

async def unban_simulator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Uso correcto: `/unban +51999888777`")
        return
        
    target_number = " ".join(context.args)
    msg = await update.message.reply_text(f"📩 Redactando correo de apelación simulado para {target_number}...")
    await asyncio.sleep(2)
    await msg.edit_text("🔑 Generando ID de soporte técnico falso...")
    await asyncio.sleep(2)
    await msg.edit_text("🔄 Modificando estado en la base de datos simulada...")
    await asyncio.sleep(1.5)
    await msg.edit_text(f"✅ **Simulación de Unban terminada**\n\nSe ha enviado la solicitud ficticia de reactivación para {target_number}.")

async def check_simulator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Uso correcto: `/check +51999888777`")
        return
        
    target_number = " ".join(context.args)
    msg = await update.message.reply_text(f"🔎 Analizando metadatos públicos de {target_number}...")
    await asyncio.sleep(2)
    
    antiban = random.choice(["Activado ✅", "Desactivado ❌"])
    vulnerabilidad = random.choice(["Baja", "Media", "Alta ⚠️"])
    
    await msg.edit_text(
        f"📊 **REPORTE SIMULADO DE SEGURIDAD**\n\n"
        f"📱 **Número:** {target_number}\n"
        f"🛡️ **Protección Antiban:** {antiban}\n"
        f"☣️ **Vulnerabilidad a Spam:** {vulnerabilidad}\n\n"
        f"_Nota: Datos generados aleatoriamente con fines lúdicos._",
        parse_mode="Markdown"
    )

def main():
    if not TOKEN:
        print("Error crítico: Variable TELEGRAM_TOKEN no configurada.")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("ban", ban_simulator))
    app.add_handler(CommandHandler("unban", unban_simulator))
    app.add_handler(CommandHandler("check", check_simulator))
    
    print("El simulador está corriendo...")
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(app.initialize())
    loop.run_until_complete(app.updater.start_polling())
    loop.run_until_complete(app.start())
    
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(app.stop())
        loop.run_until_complete(app.updater.stop())
        loop.run_until_complete(app.shutdown())

if __name__ == "__main__":
    main()
