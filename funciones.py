from menu import MENSANJE_INTRO
from database import *

def _pedir_id():
    mostrar()
    id_eleccion = input("\nDame el ID de la tarea: ")
    return int(id_eleccion)

# Ver

def mostrar_uno():
    _id = _pedir_id()
    tarea = Task.get(_id)
    print(f"""
Mostrando la tarea {_id}
------------------------
ID: {_id}
Creada en: {tarea.created_at}
Completada: {"Si" if tarea.completed else "No"}
Descripcion: {tarea.description}
""")

# Mostrar

def mostrar():
    for tarea in Task.all():
        print(f"{tarea.id} - {tarea.description}")
    print()


# Crear

def crear():
    descripcion = input("Dame una descripcion para la nueva tarea: ")
    Task(descripcion).save()

# Cambiar

def cambiar():
    _id = _pedir_id()
    tarea = Task.get(_id)
    descripcion_nueva = input(f"La tarea es {tarea.description}, dame una nueva descripcion\n\t> ")
    tarea.description = descripcion_nueva
    if input("Quieres marcarla como completada?\n\t(y/n) > ").lower() in ("y", "yes", "si"):
        tarea.completed = True
    tarea.save()

# Eliminar

def eliminar():
    _id = _pedir_id()
    tarea = Task.get(_id)
    tarea.delete()

# Bucle de menu

dicc_elecciones = {
    "VER": mostrar_uno,
    "MOSTRAR": mostrar,
    "CREAR": crear,
    "CAMBIAR": cambiar,
    "ELIMINAR": eliminar
}

def bucle_menu():
    while True:
        print(MENSANJE_INTRO)
        eleccion = input("\t> ").upper()
        print()
        if eleccion == "SALIR":
            return None
        else:
            try:
                dicc_elecciones[eleccion]()
                input("Presiona una tecla para volver al menu")
            except Exception as error:
                print(repr(error))
