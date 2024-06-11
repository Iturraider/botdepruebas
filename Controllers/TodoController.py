from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters, CallbackContext, CallbackQueryHandler
import random

from Models.Todo import Todo
from Models.TodoList import todo_list, crear_grupos

OBTENER_GRUPOS, PRUEBA_OTRA_VEZ = range(2)

class TodoController:

    @staticmethod
    async def add_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        command = update.message.text.split()[0]
        title = "".join( update.message.text.split(command)[1])
        todo_list.append( Todo(title))
        await update.message.reply_text("Nota agregada")

    @staticmethod
    async def list_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if(len(todo_list) == 0):
            await update.message.reply_text("No hay tareas todavía")
            return
        answer = ""
        for i, todo in enumerate(todo_list):
            answer = answer + f"{i + 1} - { '✅' if todo.is_completed else '⭕️'} {todo.title} \n"
        await update.message.reply_text(answer)


    @staticmethod
    async def check_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        index = int(context.args[0])
        if(index > len(todo_list) or index <= 0):
            await update.message.reply_text("ERROR, esa tarea no existe")
            return
        todo_list[index - 1].set_completed()
        await update.message.reply_text(f"La tarea {index} ha sido completada")
        await TodoController.list_todo(update, context)

    @staticmethod
    async def clear_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        todo_list.clear()
        await update.message.reply_text("La lista ha sido limpiada")
    @staticmethod
    async def mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Esto es un mensaje de texto")
        # await update.message.reply_photo(photo="https://ellibrodepython.com/assets/images/el-libro-de-python.png")
        # await update.message.reply_audio(audio="Grabación.m4a")
        # await update.message.reply_video_note(video_note="Prueba de vídeo.mp4")
        # await update.message.reply_document(document="Características y necesidades sociales y emocionales del alumnado más capaz.pdf")
        # await update.message.reply_voice(voice="Grabación.m4a")
        # await update.message.reply_text("https://ellibrodepython.com/assets/images/el-libro-de-python.png")
        # await update.message.reply_animation(animation="beating-up-beat-up.mp4")
        # await update.message.reply_sticker(sticker="sticker cs1.webp")
        # await update.message.reply_chat_action("typing")
        # await update.message.reply_chat_action("upload_photo")
        # await update.message.reply_chat_action("upload_video")
        # await update.message.reply_chat_action("upload_audio")
        # await update.message.reply_chat_action("upload_document")
        # await update.message.reply_chat_action("upload_voice")
        # await update.message.reply_chat_action("upload_video_note")
        # await update.message.reply_chat_action("upload_media")


class GruposComunidad:

    

    @staticmethod
    async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        keyboard = ReplyKeyboardMarkup([
        [KeyboardButton(text="2"), KeyboardButton(text="3")],
        [KeyboardButton(text="4"), KeyboardButton(text="5")]
    ])

        await update.message.reply_text("Hola, bienvenido al bot para crear grupos de la comunidad")
        await update.message.reply_text("¿Cuantos grupos quieres Hacer?", reply_markup=keyboard)
        return OBTENER_GRUPOS

    @staticmethod
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

    @staticmethod
    async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Has dejado la conversación")
        return ConversationHandler.END

    @staticmethod
    async def numero_grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("¿Cuantos grupos quieres hacer?")
        return OBTENER_GRUPOS

    @staticmethod
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
                return ConversationHandler.END
            else:
                await update.message.reply_text("Por favor, ingresa un número válido.")
        except ValueError:
            await update.message.reply_text("Por favor, ingresa un número válido.")
            return

        # Suggested code may be subject to a license. Learn more: ~LicenseLog:910095168.
        return ConversationHandler.END

