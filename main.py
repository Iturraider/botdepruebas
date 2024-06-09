from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters, CallbackContext, CallbackQueryHandler
from Controllers.TodoController import TodoController
import random

TOKEN = "7132677914:AAE36FvjLsMky3AQgTBA8kPflSzrHjWQrXw"




OBTENER_NOMBRE, OBTENER_APELLIDOS = range(2)

OBTENER_GRUPOS, PRUEBA_OTRA_VEZ = range(2)

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        keyboard = ReplyKeyboardMarkup([
        [KeyboardButton(text="2"), KeyboardButton(text="3")],
        [KeyboardButton(text="4"), KeyboardButton(text="5")]
    ])

        await update.message.reply_text("Hola, bienvenido al bot para crear grupos de la comunidad")
        await update.message.reply_text("¿Cuantos grupos quieres Hacer?", reply_markup=keyboard)
        return OBTENER_GRUPOS

async def boton_callback(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    numero = update.callback_query.data
    message = ""
    lista = ["Jose y Laura", "Andrés y Salut", "Javi y Salut", "Luján y Sergio"," Enan y Pilar", "David y Sandra", "Marcos y Maria", "Ana María y Salva", "Joan", "Cristina", "Maria"]

    mensaje = f"Vale, voy a hacer {numero} grupos de comunidad"
    await update.callback_query.message.reply_text(mensaje)

    grupos_creados = crear_grupos(int(numero), lista)
                
    for i, grupo in enumerate(grupos_creados):
        message += f"Grupo {i+1}: {', '.join(grupo)}\n"
    await update.callback_query.message.reply_text(message)
    # await update.callback_query.message.reply_text(numero)

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

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Has dejado la conversación")
    return ConversationHandler.END

info_conversation_handler = ConversationHandler(
        entry_points=[ CommandHandler("data", pedir_nombre)],
        states={
            OBTENER_NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener_nombre)],
            OBTENER_APELLIDOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener_apellidos)]
        },
        fallbacks=[ CommandHandler("cancel", cancel_conversation)]
    )


def crear_grupos(numero_grupos, lista_nombres):
        """
        Función que crea grupos a partir de una lista de nombres.
        Args:
            numero_grupos: El número de grupos a crear.
            lista_nombres: Una lista de nombres.
        Returns:
            Una lista de listas, donde cada sublista representa un grupo.
        """
        random.shuffle(lista_nombres)  # Mezclamos los nombres aleatoriamente
        grupos = []
        for i in range(numero_grupos):
            grupos.append([])
        # Distribuimos los nombres en los grupos
        for i, nombre in enumerate(lista_nombres):
            grupo_index = i % numero_grupos
            grupos[grupo_index].append(nombre)
        return grupos


async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Has dejado la conversación")
        return ConversationHandler.END
async def numero_grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("¿Cuantos grupos quieres hacer?")
        return OBTENER_GRUPOS
    
async def obtener_grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["groups"] = update.message.text

        try:
            numero = int(context.user_data['groups'])
        
            mensaje = ""
            message = ""
            lista = ["Jose y Laura", "Andrés y Salut", "Javi y Salut", "Luján y Sergio"," Enan y Pilar", "David y Sandra", "Marcos y Maria", "Ana María y Salva", "Joan", "Cristina", "Maria"]
            
            if numero >= 0:
                mensaje = f"Vale, voy a hacer {numero} grupos de comunidad"
                await update.message.reply_text(mensaje)

                grupos_creados = crear_grupos(numero, lista)
                
                for i, grupo in enumerate(grupos_creados):
                    message += f"Grupo {i+1}: {', '.join(grupo)}\n"
                await update.message.reply_text(message)
        except ValueError:
            await update.message.reply_text("Por favor, ingresa un número válido.")
            return 

# Suggested code may be subject to a license. Learn more: ~LicenseLog:910095168.
        return ConversationHandler.END
    





application = ApplicationBuilder().token(TOKEN).build()

# application.add_handler( CommandHandler( "start",  say_hello) )

application.add_handler( CallbackQueryHandler(boton_callback) )



grupos_conversation_handler = ConversationHandler(
        entry_points=[ CommandHandler("start", say_hello), CommandHandler("crear", say_hello)],
        states={
            OBTENER_GRUPOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener_grupos)],
# Suggested code may be subject to a license. Learn more: ~LicenseLog:3306488876.
            PRUEBA_OTRA_VEZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, numero_grupos)]

        },
        fallbacks=[ CommandHandler("cancel", cancel_conversation)]
    )


application.add_handler( CommandHandler( "add",  TodoController.add_todo) )
application.add_handler( CommandHandler( "list", TodoController.list_todo) )
application.add_handler( CommandHandler( "check", TodoController.check_todo) )
application.add_handler( CommandHandler( "clear", TodoController.clear_todo) )
application.add_handler( CommandHandler( "mensajes", TodoController.mensajes) )

# application.add_handler( MessageHandler( filters.TEXT & ~filters.AUDIO, send_message ))

application.add_handler(grupos_conversation_handler)

application.run_polling(allowed_updates=Update.ALL_TYPES)