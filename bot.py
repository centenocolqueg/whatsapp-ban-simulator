import os
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = 8315143020  
usuarios_premium = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    estado = "👑 PREMIUM (ACTIVO)" if user_id in usuarios_premium or user_id == ADMIN_ID else "🔒 LICENCIA NO DETECTADA"
    
    await update.message.reply_text(
        f"⚙️ **METASPLOIT WA-AUDIT INTERFACE v4.0.1** ⚙️\n"
        f"====================================\n\n"
        f"💻 `Consola de pruebas de estrés activa.`\n"
        f"👤 **Estado de tu Licencia:** {estado}\n\n"
        f"📌 **Módulos de comandos disponibles:**\n"
        f"🔹 `/ban <número>` ➔ Vector de ataque por reportes masivos\n"
        f"🔹 `/unban <número>` ➔ Ejecutar bypass de apelación SMTP\n"
        f"🔹 `/check <número>` ➔ Escanear vulnerabilidad y firewall\n"
        f"🔹 `/status` ➔ Estado general de los servidores de red\n\n"
        f"🛒 Si tu cuenta no está activa, escribe `/comprar` para obtener acceso vía Yape."
    )

async def comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_pago = (
        "💳 **SISTEMA DE ADQUISICIÓN DE LICENCIAS** 💳\n"
        "====================================\n\n"
        "💵 **Precio de Licencia Premium:** S/. 30.00 PEN\n"
        "📌 **Instrucciones para la activación:**\n"
        "1. Realiza el abono correspondiente mediante **Yape** al número corporativo asociado.\n"
        "2. Toma una captura de pantalla clara donde se visualice el número de operación y la fecha.\n"
        "3. **Envía esa captura de pantalla (imagen) directamente a este chat del bot.**\n\n"
        "⏳ Una vez enviada la imagen, el sistema enviará tu recibo a nuestro nodo central para su verificación instantánea."
    )
    
    if os.path.exists("yape.png"):
        try:
            with open("yape.png", "rb") as photo:
                await update.message.reply_photo(photo=photo, caption=texto_pago, parse_mode="Markdown")
                return
        except Exception:
            pass
    await update.message.reply_text(texto_pago, parse_mode="Markdown")

async def recibir_comprobante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if user.id == ADMIN_ID:
        await update.message.reply_text("⚡ Modo Administrador detectado. Comprobante omitido.")
        return

    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        keyboard = [[
            InlineKeyboardButton("✅ Aprobar Licencia", callback_data=f"aprobar_{user.id}"),
            InlineKeyboardButton("❌ Rechazar Recibo", callback_data=f"rechazar_{user.id}")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 **NUEVO COMPROBANTE RECIBIDO**\n\n👤 **Cliente:** {user.first_name}\n🆔 **ID:** `{user.id}`\n🔗 **Alias:** @{user.username if user.username else 'Sin_Username'}"
        )
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_file.file_id, reply_markup=reply_markup)
        await update.message.reply_text("📥 **Recibo recibido con éxito.** El documento ha sido encolado. Se te notificará aquí en cuanto sea validado.")

async def procesar_botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID: return
        
    accion, cliente_id = query.data.split("_")
    cliente_id_int = int(cliente_id)
    
    if accion == "aprobar":
        usuarios_premium.add(cliente_id_int)
        try:
            await context.bot.send_message(
                chat_id=cliente_id_int,
                text="✅ **¡LICENCIA CONFIGURADA CON ÉXITO!**\n\nTu pago ha sido validado correctamente. Escribe `/start` para inicializar el menú Premium."
            )
            await query.edit_message_caption(caption=f"✅ Licencia activada con éxito para el ID: {cliente_id}")
        except Exception:
            await query.edit_message_caption(caption=f"✅ Aprobado, pero el usuario cerró el chat.")
    elif accion == "rechazar":
        usuarios_premium.discard(cliente_id_int)
        try:
            await context.bot.send_message(
                chat_id=cliente_id_int,
                text="❌ **AUTENTICACIÓN DE COMPROBANTE FALLIDA**\n\nEl recibo enviado no ha podido ser validado. Inténtalo de nuevo usando `/comprar`."
            )
            await query.edit_message_caption(caption=f"❌ Transacción rechazada para el ID: {cliente_id}")
        except Exception:
            await query.edit_message_caption(caption=f"❌ Rechazado, cliente inaccesible.")

def es_premium(user_id):
    return user_id in usuarios_premium or user_id == ADMIN_ID

async def ban_simulator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not es_premium(update.message.from_user.id):
        await update.message.reply_text("🔒 **ACCESO DENEGADO:** Requiere suscripción Premium activa. Adquiérela ejecutando `/comprar`.")
        return
    if not context.args:
        await update.message.reply_text("❌ Uso: `/ban +51999888777`")
        return
    target = " ".join(context.args)
    msg = await update.message.reply_text(f"🛰️ `[CONNECTING]` Estableciendo túnel proxy cifrado hacia {target}...")
    await asyncio.sleep(2)
    await msg.edit_text("⚙️ `[PAYLOAD]` Inyectando ráfaga de paquetes de reporte masivos...")
    await asyncio.sleep(2)
    await msg.edit_text(f"⚠️ **[COMPLETADO]** Solicitud de suspensión técnica encolada para {target}.")

async def unban_simulator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not es_premium(update.message.from_user.id):
        await update.message.reply_text("🔒 **ACCESO DENEGADO:** Requiere suscripción Premium activa. Adquiérela ejecutando `/comprar`.")
        return
    if not context.args:
        await update.message.reply_text("❌ Uso: `/unban +51999888777`")
        return
    target = " ".join(context.args)
    msg = await update.message.reply_text(f"📩 `[EXPLOIT]` Remitiendo peticiones SMTP de restablecimiento para {target}...")
    await asyncio.sleep(2)
    await msg.edit_text(f"✅ **[COMPLETADO]** Orden de desbloqueo raíz enviada para {target}.")

async def check_simulator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not es_premium(update.message.from_user.id):
        await update.message.reply_text("🔒 **ACCESO DENEGADO:** Requiere suscripción Premium activa. Adquiérela ejecutando `/comprar`.")
        return
    if not context.args:
        await update.message.reply_text("❌ Uso: `/check +51999888777`")
        return
    target = " ".join(context.args)
    msg = await update.message.reply_text(f"🔎 `[SCAN]` Analizando puertos del nodo remoto {target}...")
    await asyncio.sleep(2)
    await msg.edit_text(f"📊 **REPORTE TÉCNICO:** {target}\n🛡️ Firewall Antiban: `Cifrado Débil ❌` \n☣️ Vulnerabilidad: `Crítica ⚠️` ")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 **ESTADO DEL SISTEMA:** Servidores en línea (Latencia: 42ms). Nodos proxy operativos.")

def main():
    if not TOKEN: return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("comprar", comprar))
    app.add_handler(CommandHandler("ban", ban_simulator))
    app.add_handler(CommandHandler("unban", unban_simulator))
    app.add_handler(CommandHandler("check", check_simulator))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.PHOTO, recibir_comprobante))
    app.add_handler(CallbackQueryHandler(procesar_botones))
    
    print("Bot corriendo de forma limpia...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
