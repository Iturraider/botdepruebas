from Models.Todo import Todo
import random


todo_list: list[Todo] = []

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