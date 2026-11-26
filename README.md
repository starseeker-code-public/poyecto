# Proyecto

## Paquete de base de datos (`database/`)

Persistencia en SQLite para tareas, abstraída tras una sencilla clase `Task`.
Impórtala desde cualquier módulo de la raíz del proyecto (p. ej. `main.py`); no
requiere configuración: el archivo de base de datos y la tabla se crean
automáticamente en el primer uso.

Requiere Python 3.10+ (usa solo la biblioteca estándar).

### Estructura

| Archivo | Propósito |
|---------|-----------|
| `database/db.py` | Funciones de bajo nivel de SQLite (crear / leer / actualizar / eliminar). |
| `database/task.py` | Clase `Task` que envuelve esas funciones en métodos. |
| `database/__init__.py` | Expone la API pública para poder hacer `from database import ...`. |

La base de datos se guarda en `tasks.db` en la raíz del proyecto (ignorado por git).

### Campos de Task

| Campo | Tipo | Notas |
|-------|------|-------|
| `id` | `int` | Generado automáticamente por SQLite. `None` hasta que la tarea se guarda. |
| `created_at` | `datetime` | Se establece automáticamente en el primer guardado (precisión de segundos). |
| `completed` | `bool` | Por defecto `False`. |
| `description` | `str` | Texto obligatorio. |

### Uso

```python
from database import Task

# Crear
task = Task.create("Buy milk")        # la construye, guarda y devuelve (con id y created_at rellenados)
other = Task("Walk the dog").save()   # lo mismo en dos pasos

# Leer
Task.get(1)                           # Task, o None si no existe
Task.all()                            # lista de todas las tareas, ordenadas por id
Task.all(completed=False)             # solo las pendientes (True = solo las completadas)

# Actualizar: cambia atributos y luego llama a save()
task.description = "Buy oat milk"
task.completed = True
task.save()

# Eliminar
task.delete()                         # True si se eliminó una fila; task.id pasa a ser None
```

### API de `Task`

| Miembro | Descripción |
|---------|-------------|
| `Task(description, completed=False, id=None, created_at=None)` | Construye una tarea en memoria (aún sin guardar). |
| `Task.create(description, completed=False)` | Construye y guarda en un solo paso. |
| `task.save()` | Hace INSERT si la tarea no tiene `id`; en caso contrario, UPDATE. Devuelve `self`. Lanza `LookupError` si la fila ya no existe. |
| `Task.get(task_id)` | Obtiene una tarea, o `None`. |
| `Task.all(completed=None)` | Obtiene todas las tareas, opcionalmente filtradas por `completed`. |
| `task.refresh()` | Recarga los campos de la tarea desde la base de datos. Lanza `LookupError` si ya no existe. |
| `task.delete()` | Elimina la fila. Devuelve `True` si existía. |

### Funciones directas

Si prefieres trabajar sin la clase, las funciones subyacentes también se pueden
importar desde `database`. Devuelven diccionarios simples
(`{"id", "created_at", "completed", "description"}`):

```python
from database import create_task, get_task, get_all_tasks, update_task, delete_task

t = create_task("Buy milk")                 # -> dict
get_task(t["id"])                           # -> dict | None
get_all_tasks(completed=False)              # -> list[dict]
update_task(t["id"], completed=True)        # -> bool (False si no se encuentra el id); los campos None no se modifican
delete_task(t["id"])                        # -> bool
```

### Usar un archivo de base de datos distinto

```python
import database
database.set_db_path("other.db")   # llámalo antes que cualquier otra función de database
```

`":memory:"` no está soportado, porque cada función abre su propia conexión;
usa un archivo temporal para las pruebas.
