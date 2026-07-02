import os
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Token de acceso de Telegram (Gestionado por Render)
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# ID de Administrador verificado
ADMIN_ID = 8315143020  

# Registro temporal en caché para usuarios con licencia aprobada
usuarios_premium = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Interfaz principal del sistema con verificación de privilegios"""
    user_id = update.message.from_user.id
    estado_cuenta = "👑 PREMIUM (ACTIVO)" if user_id in usuarios_premium or user_id == ADMIN_ID else "🔒 LICENCIA NO DETECTADA"
    
    await update.message.reply_text(
        f"⚙️ **METASPLOIT WA-AUDIT INTERFACE v4.0.1** ⚙️\n"
        f"====================================\n\n"
        f"💻 `Consola de pruebas de estrés activa.`\n"
        f"👤 **Estado de tu Licencia:** {estado_cuenta}\n\n"
        f"📌 **Módulos de comandos disponibles:**\n"
        f"🔹 `/ban <número>` ➔ Vector de ataque por reportes masivos\n"
        f"🔹 `/unban <número>` ➔ Ejecutar bypass de apelación SMTP\n"
        f"🔹 `/check <número>` ➔ Escanear vulnerabilidad y firewall\n"
        f"🔹 `/status` ➔ Estado general de los servidores de red\n\n"
        f"🛒 Si tu cuenta no está activa, escribe `/comprar` para obtener acceso vía Yape."
    )

async def comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Módulo de pagos que despliega el costo de 30 Soles y las instrucciones de Yape"""
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
    
    # Comprobación del archivo yape.png en el repositorio
    if os.path.exists("yape.png"):
        try:
            await update.message.reply_photo(photo=open("yape.png", "rb"), caption=texto_pago, parse_mode="Markdown")
            return
        except Exception:
            pass
    await update.message.reply_text(texto_pago, parse_mode="Markdown")

async def recibir_comprobante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Intercepta imágenes de los clientes y las enruta a tu chat privado con paneles de decisión"""
    user = update.message.from_user
    
    if user.id == ADMIN_ID:
        await update.message.reply_text("⚡ Modo Administrador detectado. Comprobante de prueba omitido.")
        return

    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        
        # Inyección de teclado interactivo en tu chat privado
        keyboard = [
            [
                InlineKeyboardButton("✅ Aprobar Licencia", callback_data=f"aprobar_{user.id}"),
                InlineKeyboardButton("❌ Rechazar Recibo", callback_data=f"rechazar_{user.id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 **NUEVO COMPROBANTE ENVIADO A REVISIÓN**\n\n"
                 f"👤 **Cliente:** {user.first_name}\n"
                 f"🆔 **ID de Usuario:** `{user.id}`\n"
                 f"🔗 **Alias:** @{user.username if user.username else 'Sin_Username'}\n"
                 f"📋 _Verifica tu aplicación de Yape antes de presionar el botón._"
        )
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_file.file_id,
            reply_markup=reply_markup
        )
        
        await update.message.reply_text("📥 **Recibo recibido con éxito.** El documento ha sido encolado en nuestro sistema de soporte técnico. Se te notificará en este chat en cuanto sea validado.")

async def procesar_botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mapea los eventos de clic en los botones de aprobación de tu chat"""
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != ADMIN_ID:
        return
        
    accion, cliente_id = query.data.split("_")
    cliente_id_int = int(cliente_id)
    
    if accion == "aprobar":
        usuarios_premium.add(cliente_id_int)
        
        try:
            await context.bot.send_message(
                chat_id=cliente_id_int,
                text="✅ **¡LICENCIA CONFIGURADA CON ÉXITO!**\n\n"
                     "Tu pago ha sido validado correctamente en la base de datos raíz.\n"
                     "Los módulos de auditoría ya están desbloqueados. Escribe `/start` para inicializar el menú de comandos Premium."
            )
            await query.edit_message_caption(caption=f"✅ Licencia activada con éxito para el ID: {cliente_id}")
        except Exception:
            await query.edit_message_caption(caption=f"✅ Aprobado, pero el usuario no pudo ser notificado (Chat cerrado).")
            
    elif accion == "rechazar":
        usuarios_premium.discard(cliente_id_int)
        
        try:
            await context.bot.send_message(
                chat_id=cliente_id_int,
                text="❌ **AUTENTICACIÓN DE COMPROBANTE FALLIDA**\n\n"
                     "El recibo de Yape enviado no ha podido ser validado en el sistema de cuentas (monto incorrecto o inexistente).\n"
                     "Si consideras que es un error, genera un nuevo intento con una captura válida usando `/comprar`."
            )
            await query.edit_message_caption(caption=f"❌ Transacción rechazada para el ID: {cliente_id}")
        except Exception:
            await query.edit_message_caption(caption=f"❌ Rechazado, cliente inaccesible.")

def es_premium(user_id):
    return user_id in usuarios_premium or user_id == ADMIN_ID

async def ban_simulator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Vector de comandos bajo demanda de auditoría"""
    user_id = update.message.from_user.id
    if not es_premium(user_id):
        await update.message.reply_text("🔒 **ACCESO DENEGADO:** Este comando requiere una suscripción Premium activa. Adquiérela ejecutando `/comprar`.")
        return
        
    if not context.args:
        await update.message.reply_text("❌ `ERROR: Falta el número objetivo.` Uso: `/ban +51999888777`")
        return
    
    target_number = " ".join(context.args)
    msg = await update.message.reply_text(f"🛰️ `[CONNECTING]` Estableciendo túnel proxy cifrado hacia {target_number}...")
    await asyncio.sleep(2)
    await msg.edit_text("⚙️ `[PAYLOAD]` Inyectando ráfaga de paquetes de reporte masivos...")
    await asyncio.sleep(2)
    await msg.edit_text(f"⚠️ **[COMPLETADO]** Solicitud de suspensión técnica encolada para {target_number}.")

async def unban_simulator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Módulo de bypass de soporte"""
    user_id = update.message.from_user.id
    if not es_premium(user_id):
        await update.message.reply_text("🔒 **ACCESO DENEGADO:** Este comando requiere una suscripción Premium activa. Adquiérela ejecutando `/comprar`.")
        return
        
    if not context.args:
        await update.message.reply_text("❌ `ERROR: Falta el número objetivo.` Uso: `/unban +51999888777`")
        return
        
    target_number = " ".join(context.args)
    msg = await update.message.reply_text(f"📩 `[EXPLOIT]` Remitiendo peticiones SMTP de restablecimiento para {target_number}...")
    await asyncio.sleep(2)
    await msg.edit_text(f"✅ **[COMPLETADO]** Orden de desbloqueo raíz enviada para {target_number}.")

async def check_simulator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Escáner de vulnerabilidades de red"""
    user_id = update.message.from_user.id
    if not es_premium(user_id):
        await update.message.reply_text("🔒 **ACCESO DENEGADO:** Este comando requiere una suscripción Premium activa. Adquiérela ejecutando `/comprar`.")
        return
        
    if not context.args:
        await update.message.reply_text("❌ `ERROR: Falta el número objetivo.` Uso: `/check +51999888777`")
        return
        
    target_number = " ".join(context.args)
    msg = await update.message.reply_text(f"🔎 `[SCAN]` Analizando puertos del nodo remoto {target_number}...")
    await asyncio.sleep(2)
    await msg.edit_text(f"📊 **REPORTE TÉCNICO:** {target_number}\n🛡️ Firewall Antiban: `Cifrado Débil (Vulnerable) ❌` \n☣️ Vulnerabilidad: `Crítica ⚠️` ")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 **ESTADO DEL SISTEMA:** Servidores en línea (Latencia: 42ms). Nodos proxy operativos.")

def main():
    if not TOKEN:
        print("Error crítico: Variable TELEGRAM_TOKEN no configurada.")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("comprar", comprar))
    app.add_handler(CommandHandler("ban", ban_simulator))
    app.add_handler(CommandHandler("unban", unban_simulator))
    app.add_handler(CommandHandler("check", check_simulator))
    app.add_handler(CommandHandler("status", status))
    
    app.add_handler(MessageHandler(filters.PHOTO, recibir_comprobante))
    app.add_handler(CallbackQueryHandler(procesar_botones))
    
    print("El sistema con pasarela Yape integrada está corriendo...")
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
