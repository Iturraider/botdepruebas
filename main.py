from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters, CallbackContext, CallbackQueryHandler
from Controllers.TodoController import TodoController, GruposComunidad, OBTENER_GRUPOS, PRUEBA_OTRA_VEZ


TOKEN = "7132677914:AAE36FvjLsMky3AQgTBA8kPflSzrHjWQrXw"


OBTENER_NOMBRE, OBTENER_APELLIDOS = range(2)

async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Has escrito un mensaje")

async def pedir_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dime tu nombre por favor")
    return OBTENER_NOMBRE

async def obtener_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Dime tus apellidos")
    return OBTENER_APELLIDOS

async def obtener_apellidos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["last_name"] = update.message.text
    await update.message.reply_text(f"""Gracias, tus datos son Nombre: {context.user_data['name']} Apellido: {context.user_data['last_name']}""")
    return ConversationHandler.END



# info_conversation_handler = ConversationHandler(
#         entry_points=[ CommandHandler("data", pedir_nombre)],
#         states={
#             OBTENER_NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener_nombre)],
#             OBTENER_APELLIDOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener_apellidos)]
#         },
#         fallbacks=[ CommandHandler("cancel", cancel_conversation)]
#     )





application = ApplicationBuilder().token(TOKEN).build()

# application.add_handler( CommandHandler( "start",  say_hello) )

application.add_handler( CallbackQueryHandler(GruposComunidad.boton_callback) )



grupos_conversation_handler = ConversationHandler(
        entry_points=[ CommandHandler("start", GruposComunidad.say_hello), CommandHandler("crear", GruposComunidad.say_hello)],
        states={
            OBTENER_GRUPOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, GruposComunidad.obtener_grupos)],
# Suggested code may be subject to a license. Learn more: ~LicenseLog:3306488876.
            PRUEBA_OTRA_VEZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, GruposComunidad.numero_grupos)]

        },
        fallbacks=[ CommandHandler("cancel", GruposComunidad.cancel_conversation)]
    )


application.add_handler( CommandHandler( "add",  TodoController.add_todo) )
application.add_handler( CommandHandler( "list", TodoController.list_todo) )
application.add_handler( CommandHandler( "check", TodoController.check_todo) )
application.add_handler( CommandHandler( "clear", TodoController.clear_todo) )
application.add_handler( CommandHandler( "mensajes", TodoController.mensajes) )

# application.add_handler( MessageHandler( filters.TEXT & ~filters.AUDIO, send_message ))

application.add_handler(grupos_conversation_handler)

application.run_polling(allowed_updates=Update.ALL_TYPES)