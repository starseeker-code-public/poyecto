from database import *
from datetime import datetime

# Tests de clase Task

# Create + Read

Task.create("Tarea 1")
Task("Tarea 2", completed=True).save()
total = Task.all()

assert len(total) == 2
assert total[0].description == "Tarea 1"
assert total[1].description == "Tarea 2"
assert total[0].completed is False
assert total[1].completed is True
assert total[0].created_at > datetime(2026, 11, 25)

# Update

tarea_1 = Task.get(1)
tarea_1.description = "Tarea cambiada"
tarea_1.completed = True
tarea_1.save()

total = Task.all()
assert len(total) == 2
assert total[0].description != "Tarea 1"
assert total[0].description == "Tarea cambiada"
assert total[0].completed is True

# Delete

for tarea in total:
    tarea.delete()
total = Task.all()

assert len(total) == 0

# Limpieza
