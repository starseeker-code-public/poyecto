from database import *
from datetime import datetime
import unittest
import pathlib


# Setup
class TestTarea(unittest.TestCase):
    def setUp(self):
        Task.create("Tarea 1")
        Task("Tarea 2", completed=True).save()

    def test_crear(self):
        total = Task.all()
        self.assertEqual(len(total), 2)
        self.assertEqual(total[0].description, "Tarea 1")
        self.assertEqual(total[1].description, "Tarea 2")
        self.assertFalse(total[0].completed)
        self.assertTrue(total[1].completed)
        self.assertGreater(total[0].created_at, datetime(2026, 11, 25))

    def test_modificar(self):
        tarea = Task.get(1)
        tarea.description = "Tarea cambiada"
        tarea.completed = True
        tarea.save()
        total = Task.all()
        self.assertEqual(len(total), 2)
        self.assertNotEqual(total[0].description, "Tarea 1")
        self.assertEqual(total[0].description, "Tarea cambiada")
        self.assertTrue(total[0].completed)

    def test_delete(self):
        total = Task.all()
        for tarea in total:
            tarea.delete()
        total = Task.all()
        self.assertEqual(len(total), 0)

    def tearDown(self):
        ruta_db = pathlib.Path("tasks.db")
        ruta_db.unlink()

if __name__ == '__main__':
    unittest.main()