from telegram import Update
from telegram.ext import ContextTypes

from Models.Todo import Todo
from Models.TodoList import todo_list

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
        await update.message.reply_photo(photo="https://ellibrodepython.com/assets/images/el-libro-de-python.png")
        await update.message.reply_audio(audio="Grabación.m4a")
        await update.message.reply_video(video="Grabación.m4a")
        await update.message.reply_document(document="Características y necesidades sociales y emocionales del alumnado más capaz.pdf")
        await update.message.reply_voice(voice="Grabación.m4a")
        await update.message.reply_text("https://www.youtube.com/watch?v=9gnIvTUJIuY&list=PL1-d6o0SXOR4_b2alX7VDkvxmfSxvKygd&index=8")
