import sqlite3

class DatabaseManager:
    def __init__(self, db_name='ecole.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Table étudiants
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                date_naissance TEXT,
                nationalite TEXT,
                sexe TEXT,
                statut TEXT,
                classe_id INTEGER,
                FOREIGN KEY (classe_id) REFERENCES classes(id)
            )
        ''')

        # Table parents
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS parents (
                id INTEGER PRIMARY KEY,
                type TEXT,  -- 'père' ou 'mère'
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                tel1 TEXT NOT NULL,
                tel2 TEXT,
                email TEXT NOT NULL
            )
        ''')

        # Table de liaison étudiants-parents
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_parent (
                student_id INTEGER,
                parent_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (parent_id) REFERENCES parents(id),
                PRIMARY KEY (student_id, parent_id)
            )
        ''')

        # Table frais de scolarité
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS frais_scolarite (
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                total_annee REAL,
                bourse_pourcentage REAL,
                frais_inscription REAL,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        ''')

        # Table échéancier
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS echeancier (
                id INTEGER PRIMARY KEY,
                frais_id INTEGER,
                mois TEXT,
                montant REAL,
                paye BOOLEAN,
                FOREIGN KEY (frais_id) REFERENCES frais_scolarite(id)
            )
        ''')

        # Table classes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                enseignant_id INTEGER,
                FOREIGN KEY (enseignant_id) REFERENCES enseignants(id)
            )
        ''')

        # Table enseignants
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS enseignants (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                email TEXT,
                tel TEXT
            )
        ''')

        self.conn.commit()

    # ---------------- Méthodes CRUD pour la table étudiants ----------------
    def add_student(self, student_data):
        # Méthode pour ajouter un étudiant
        self.cursor.execute('''
            INSERT INTO students (nom, prenom, date_naissance, nationalite, sexe, statut, classe_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', student_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_student(self, student_id):
        # Méthode pour récupérer les informations d'un étudiant
        self.cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        return self.cursor.fetchone()

    def update_student(self, student_id, student_data):
        # Méthode pour mettre à jour les informations d'un étudiant
        self.cursor.execute('''
            UPDATE students
            SET nom=?, prenom=?, date_naissance=?, nationalite=?, sexe=?, statut=?, classe_id=?
            WHERE id=?
        ''', student_data + (student_id,))
        self.conn.commit()

    def delete_student(self, student_id):
        # Méthode pour supprimer un étudiant
        self.cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        self.conn.commit()

    # ---------------- Méthodes CRUD pour la table parents ----------------
    def add_parent(self, parent_data):
        self.cursor.execute('''
            INSERT INTO parents (type, nom, prenom, tel1, tel2, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', parent_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_parent(self, parent_id):
        self.cursor.execute('SELECT * FROM parents WHERE id = ?', (parent_id,))
        return self.cursor.fetchone()

    def update_parent(self, parent_id, parent_data):
        self.cursor.execute('''
            UPDATE parents
            SET type=?, nom=?, prenom=?, tel1=?, tel2=?, email=?
            WHERE id=?
        ''', parent_data + (parent_id,))
        self.conn.commit()

    def delete_parent(self, parent_id):
        self.cursor.execute('DELETE FROM parents WHERE id = ?', (parent_id,))
        self.conn.commit()

    # Méthode pour lier un étudiant à un parent
    def link_student_parent(self, student_id, parent_id):
        self.cursor.execute('''
            INSERT INTO student_parent (student_id, parent_id)
            VALUES (?, ?)
        ''', (student_id, parent_id))
        self.conn.commit()

    # Méthode pour obtenir tous les parents d'un étudiant
    def get_student_parents(self, student_id):
        self.cursor.execute('''
            SELECT p.* FROM parents p
            JOIN student_parent sp ON p.id = sp.parent_id
            WHERE sp.student_id = ?
        ''', (student_id,))
        return self.cursor.fetchall()

    # Méthode pour obtenir tous les étudiants d'un parent
    def get_parent_students(self, parent_id):
        self.cursor.execute('''
            SELECT s.* FROM students s
            JOIN student_parent sp ON s.id = sp.student_id
            WHERE sp.parent_id = ?
        ''', (parent_id,))
        return self.cursor.fetchall()

    # ---------------- Méthodes CRUD pour la table frais_scolarite ---------------- 
    def add_frais_scolarite(self, frais_data):
        self.cursor.execute('''
            INSERT INTO frais_scolarite (student_id, total_annee, bourse_pourcentage, frais_inscription)
            VALUES (?, ?, ?, ?)
        ''', frais_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_frais_scolarite(self, frais_id):
        self.cursor.execute('SELECT * FROM frais_scolarite WHERE id = ?', (frais_id,))
        return self.cursor.fetchone()

    def update_frais_scolarite(self, frais_id, frais_data):
        self.cursor.execute('''
            UPDATE frais_scolarite
            SET student_id=?, total_annee=?, bourse_pourcentage=?, frais_inscription=?
            WHERE id=?
        ''', frais_data + (frais_id,))
        self.conn.commit()

    def delete_frais_scolarite(self, frais_id):
        self.cursor.execute('DELETE FROM frais_scolarite WHERE id = ?', (frais_id,))
        self.conn.commit()
    
    # ---------------- Méthodes CRUD pour la table classes ----------------
    def add_class(self, class_data):
        self.cursor.execute('''
            INSERT INTO classes (nom, enseignant_id)
            VALUES (?, ?)
        ''', class_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_class(self, class_id):
        self.cursor.execute('SELECT * FROM classes WHERE id = ?', (class_id,))
        return self.cursor.fetchone()

    def update_class(self, class_id, class_data):
        self.cursor.execute('''
            UPDATE classes
            SET nom=?, enseignant_id=?
            WHERE id=?
        ''', class_data + (class_id,))
        self.conn.commit()

    def delete_class(self, class_id):
        self.cursor.execute('DELETE FROM classes WHERE id = ?', (class_id,))
        self.conn.commit()

    # ---------------- Méthodes CRUD pour la table enseignants ----------------
    def add_teacher(self, teacher_data):
        self.cursor.execute('''
            INSERT INTO enseignants (nom, prenom, email, tel)
            VALUES (?, ?, ?, ?)
        ''', teacher_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_teacher(self, teacher_id):
        self.cursor.execute('SELECT * FROM enseignants WHERE id = ?', (teacher_id,))
        return self.cursor.fetchone()

    def update_teacher(self, teacher_id, teacher_data):
        self.cursor.execute('''
            UPDATE enseignants
            SET nom=?, prenom=?, email=?, tel=?
            WHERE id=?
        ''', teacher_data + (teacher_id,))
        self.conn.commit()

    def delete_teacher(self, teacher_id):
        self.cursor.execute('DELETE FROM enseignants WHERE id = ?', (teacher_id,))
        self.conn.commit()

    # ---------------- Méthodes CRUD pour la table echeancier ----------------
    def add_echeance(self, echeance_data):
        self.cursor.execute('''
            INSERT INTO echeancier (frais_id, mois, montant, paye)
            VALUES (?, ?, ?, ?)
        ''', echeance_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_echeance(self, echeance_id):
        self.cursor.execute('SELECT * FROM echeancier WHERE id = ?', (echeance_id,))
        return self.cursor.fetchone()

    def update_echeance(self, echeance_id, echeance_data):
        self.cursor.execute('''
            UPDATE echeancier
            SET frais_id=?, mois=?, montant=?, paye=?
            WHERE id=?
        ''', echeance_data + (echeance_id,))
        self.conn.commit()

    def delete_echeance(self, echeance_id):
        self.cursor.execute('DELETE FROM echeancier WHERE id = ?', (echeance_id,))
        self.conn.commit()

    # Méthodes supplémentaires utiles
    def get_students_in_class(self, class_id):
        self.cursor.execute('SELECT * FROM students WHERE classe_id = ?', (class_id,))
        return self.cursor.fetchall()

    def get_unpaid_fees(self):
        self.cursor.execute('''
            SELECT s.nom, s.prenom, e.mois, e.montant
            FROM students s
            JOIN frais_scolarite f ON s.id = f.student_id
            JOIN echeancier e ON f.id = e.frais_id
            WHERE e.paye = 0
        ''')
        return self.cursor.fetchall()

    def get_class_teacher(self, class_id):
        self.cursor.execute('''
            SELECT e.* FROM enseignants e
            JOIN classes c ON e.id = c.enseignant_id
            WHERE c.id = ?
        ''', (class_id,))
        return self.cursor.fetchone()

    def __del__(self):
        self.conn.close()