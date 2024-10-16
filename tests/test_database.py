import unittest
import os
from database.db_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Utiliser une base de données de test
        self.db_manager = DatabaseManager('test_ecole.db')

    def tearDown(self):
        # Supprimer la base de données de test après chaque test
        self.db_manager.__del__()
        os.remove('test_ecole.db')

    def test_add_and_get_student(self):
        student_data = ('Doe', 'John', '2000-01-01', 'Français', 'M', 'Inscription', 1)
        student_id = self.db_manager.add_student(student_data)
        retrieved_student = self.db_manager.get_student(student_id)
        self.assertEqual(retrieved_student[1:], student_data)

    def test_update_student(self):
        student_data = ('Doe', 'John', '2000-01-01', 'Français', 'M', 'Inscription', 1)
        student_id = self.db_manager.add_student(student_data)
        updated_data = ('Doe', 'Jane', '2000-01-01', 'Français', 'F', 'Réinscription', 2)
        self.db_manager.update_student(student_id, updated_data)
        retrieved_student = self.db_manager.get_student(student_id)
        self.assertEqual(retrieved_student[1:], updated_data)

    def test_delete_student(self):
        student_data = ('Doe', 'John', '2000-01-01', 'Français', 'M', 'Inscription', 1)
        student_id = self.db_manager.add_student(student_data)
        self.db_manager.delete_student(student_id)
        retrieved_student = self.db_manager.get_student(student_id)
        self.assertIsNone(retrieved_student)

    def test_add_and_get_parent(self):
        parent_data = ('père', 'Doe', 'John', '0123456789', '9876543210', 'john.doe@example.com')
        parent_id = self.db_manager.add_parent(parent_data)
        retrieved_parent = self.db_manager.get_parent(parent_id)
        self.assertEqual(retrieved_parent[1:], parent_data)

    def test_add_and_get_class(self):
        class_data = ('CM1', 1)
        class_id = self.db_manager.add_class(class_data)
        retrieved_class = self.db_manager.get_class(class_id)
        self.assertEqual(retrieved_class[1:], class_data)

    def test_add_and_get_teacher(self):
        teacher_data = ('Smith', 'Jane', 'jane.smith@example.com', '0123456789')
        teacher_id = self.db_manager.add_teacher(teacher_data)
        retrieved_teacher = self.db_manager.get_teacher(teacher_id)
        self.assertEqual(retrieved_teacher[1:], teacher_data)

    def test_add_and_get_frais_scolarite(self):
        frais_data = (1, 1000.0, 0.0, 100.0)
        frais_id = self.db_manager.add_frais_scolarite(frais_data)
        retrieved_frais = self.db_manager.get_frais_scolarite(frais_id)
        self.assertEqual(retrieved_frais[1:], frais_data)

    def test_add_and_get_echeance(self):
        echeance_data = (1, 'Septembre', 100.0, False)
        echeance_id = self.db_manager.add_echeance(echeance_data)
        retrieved_echeance = self.db_manager.get_echeance(echeance_id)
        self.assertEqual(retrieved_echeance[1:], echeance_data)

    def test_link_student_parent(self):
        student_data = ('Doe', 'John', '2000-01-01', 'Français', 'M', 'Inscription', 1)
        student_id = self.db_manager.add_student(student_data)
        parent_data = ('père', 'Doe', 'John Sr.', '0123456789', '9876543210', 'john.sr.doe@example.com')
        parent_id = self.db_manager.add_parent(parent_data)
        self.db_manager.link_student_parent(student_id, parent_id)
        student_parents = self.db_manager.get_student_parents(student_id)
        self.assertEqual(len(student_parents), 1)
        self.assertEqual(student_parents[0][1:], parent_data)

if __name__ == '__main__':
    unittest.main()