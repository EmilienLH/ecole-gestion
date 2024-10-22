import sqlite3

class DatabaseManager:
    def __init__(self, db_name='ecole.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.reset_database()

    def reset_database(self):
        self.cursor.execute('DROP TABLE IF EXISTS students')
        self.cursor.execute('DROP TABLE IF EXISTS responsables')
        self.cursor.execute('DROP TABLE IF EXISTS student_responsable')
        self.cursor.execute('DROP TABLE IF EXISTS frais_scolarite')
        self.cursor.execute('DROP TABLE IF EXISTS echeancier')
        self.cursor.execute('DROP TABLE IF EXISTS classes')
        self.cursor.execute('DROP TABLE IF EXISTS enseignants')
        self.cursor.execute('DROP TABLE IF EXISTS school_info')
        self.conn.commit()
        self.create_tables()
        self.populate_test_data()

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

        # Table responsables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS responsables (
                id INTEGER PRIMARY KEY,
                type TEXT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                tel1 TEXT NOT NULL,
                tel2 TEXT,
                email TEXT NOT NULL
            )
        ''')

        # Table de liaison étudiants-responsables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_responsable (
                student_id INTEGER,
                responsable_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (responsable_id) REFERENCES repsonsables(id),
                PRIMARY KEY (student_id, responsable_id)
            )
        ''')

        # Modification de la table frais_scolarite
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS frais_scolarite (
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                total_annee REAL,
                bourse_pourcentage REAL,
                bourse_montant REAL,
                frais_inscription REAL,
                mode_paiement TEXT,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        ''')

        # Modification de la table echeancier
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS echeancier (
                id INTEGER PRIMARY KEY,
                frais_id INTEGER,
                mois TEXT,
                montant REAL,
                paye BOOLEAN,
                type TEXT,
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
                tel TEXT,
                date_entree DATE
                contrat TEXT -- "Détaché Français", "Titulaire Gabonais", "Contractuel" 
                id_gabonais INTEGER
            )
        ''')

        # Table avec informations sur l'école
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS school_info (
                id INTEGER PRIMARY KEY,
                school_name TEXT,
                phone_number TEXT,
                email TEXT,
                director_name TEXT,
                signature BLOB
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
    
    def get_students(self):
        # Méthode pour récupérer tous les étudiants
        self.cursor.execute('SELECT * FROM students')
        return self.cursor.fetchall()

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

    # ---------------- Méthodes CRUD pour la table responsable ----------------
    def add_responsable(self, responsable_data):
        self.cursor.execute('''
            INSERT INTO responsables (type, nom, prenom, tel1, tel2, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', responsable_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_responsable(self, responsable_id):
        self.cursor.execute('SELECT * FROM responsables WHERE id = ?', (responsable_id,))
        return self.cursor.fetchone()

    def update_responsable(self, responsable_id, responsable_data):
        self.cursor.execute('''
            UPDATE responsables
            SET type=?, nom=?, prenom=?, tel1=?, tel2=?, email=?
            WHERE id=?
        ''', responsable_data + (responsable_id,))
        self.conn.commit()

    def delete_responsable(self, responsable_id):
        self.cursor.execute('DELETE FROM responsables WHERE id = ?', (responsable_id,))
        self.conn.commit()

    # Méthode pour lier un étudiant à un responsable
    def link_student_responsable(self, student_id, responsable_id):
        self.cursor.execute('''
            INSERT INTO student_responsable (student_id, responsable_id)
            VALUES (?, ?)
        ''', (student_id, responsable_id))
        self.conn.commit()

    def unlink_student_responsable(self, student_id, responsable_id):
        self.cursor.execute('''
            DELETE FROM student_responsable
            WHERE student_id = ? AND responsable_id = ?
        ''', (student_id, responsable_id))
        self.conn.commit()


    # Méthode pour obtenir tous les responsables d'un étudiant
    def get_student_responsables(self, student_id):
        self.cursor.execute('''
            SELECT r.* FROM responsables r
            JOIN student_responsable sr ON r.id = sr.responsable_id
            WHERE sr.student_id = ?
        ''', (student_id,))
        return self.cursor.fetchall()
    
    def search_responsables(self, search_text):
        self.cursor.execute('''
            SELECT id, nom, prenom
            FROM responsables
            WHERE nom LIKE ? OR prenom LIKE ?
        ''', (f'%{search_text}%', f'%{search_text}%'))
        results = self.cursor.fetchall()
        print(f"Database query results for '{search_text}': {results}")  # Debugging statement
        return results
    
    def print_responsables(self):
        self.cursor.execute('SELECT * FROM responsables')
        results = self.cursor.fetchall()
        for row in results:
            print(row)
    
    def is_responsable_linked(self, student_id, responsable_id):
        self.cursor.execute('''
            SELECT COUNT(*) FROM student_responsable
            WHERE student_id = ? AND responsable_id = ?
        ''', (student_id, responsable_id))
        count = self.cursor.fetchone()[0]
        return count > 0
    
    # ---------------- Méthodes CRUD pour la table frais_scolarite ---------------- 
    def add_frais_scolarite_manuel(self, frais_data):
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

    def get_all_classes(self):
        self.cursor.execute('SELECT * FROM classes')
        return self.cursor.fetchall

    def get_all_classes_names(self):
        self.cursor.execute('SELECT nom FROM classes')
        return self.cursor.fetchall()

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
    
    def get_echeances_by_student_id(self, student_id):
        self.cursor.execute('''
            SELECT e.id, e.frais_id, e.mois, e.montant, e.paye, e.type
            FROM echeancier e
            JOIN frais_scolarite f ON e.frais_id = f.id
            WHERE f.student_id = ?
        ''', (student_id,))
        return self.cursor.fetchall()

    def update_echeance(self, echeance_id, echeance_data):
        self.cursor.execute('''
            UPDATE echeancier
            SET frais_id=?, mois=?, montant=?, paye=?
            WHERE id=?
        ''', echeance_data + (echeance_id,))
        self.conn.commit()

    def update_echeance_payment(self, echeance_id, paye):
        self.cursor.execute('UPDATE echeancier SET paye = ? WHERE id = ?', (paye, echeance_id))
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
    
    # Méthode pour calculer les frais de scolarités : 
    def calculate_fees(self, student_id):
        student = self.get_student(student_id)
        nationalite = student[4]  

        if nationalite == 'Français' or 'Française' or 'FR':
            total_annee = 1095000
        elif nationalite == 'Gabonais' or 'Gabonaise' or 'GA':
            total_annee = 795000
        else:
            total_annee = 1245000

        frais_inscription = 100000
        return total_annee, frais_inscription

    def apply_bourse(self, total_annee, bourse_pourcentage):
        bourse_montant = total_annee * (bourse_pourcentage / 100)
        total_apres_bourse = total_annee - bourse_montant
        return total_apres_bourse, bourse_montant

    def generate_echeancier(self, frais_id, total_annee, type_inscription, mode_paiement):
        frais_inscription = 100000
        reste_a_payer = total_annee - frais_inscription
        mode_paiement = mode_paiement.lower()
        echeances = []
        echeances.append((frais_id, 'Septembre', frais_inscription, False, 'frais_inscription'))

        if mode_paiement == 'standard':
            if type_inscription == 'inscription':
                montant_echeance = reste_a_payer / 3
                for mois in ['Septembre', 'Décembre', 'Mars']:
                    echeances.append((frais_id, mois, montant_echeance, False, 'paiement_standard'))
            else:  # réinscription
                # si c'est une réinscription, les frais ont été payé l'année précédente en Juin, on les repaye pas et en Mars on les récupère
                montant_echeance = reste_a_payer / 3
                echeances.append((frais_id, 'Septembre', montant_echeance, False, 'paiement_standard'))
                echeances.append((frais_id, 'Décembre', montant_echeance, False, 'paiement_standard'))
                echeances.append((frais_id, 'Mars', montant_echeance - frais_inscription, False, 'paiement_standard'))
        elif mode_paiement == 'echéancier':
            montant_mensuel = reste_a_payer / 8
            for mois in ['Octobre', 'Novembre', 'Décembre', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai']:
                echeances.append((frais_id, mois, montant_mensuel, False, 'echéancier_mensuel'))

        return echeances

    def add_frais_scolarite(self, student_id, mode_paiement, bourse_pourcentage=0):
        total_annee, frais_inscription = self.calculate_fees(student_id)
        
        if bourse_pourcentage > 0:
            total_apres_bourse, bourse_montant = self.apply_bourse(total_annee, bourse_pourcentage)
        else:
            total_apres_bourse, bourse_montant = total_annee, 0

        self.cursor.execute('''
            INSERT INTO frais_scolarite (student_id, total_annee, bourse_pourcentage, bourse_montant, frais_inscription, mode_paiement)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (student_id, total_apres_bourse, bourse_pourcentage, bourse_montant, frais_inscription, mode_paiement))
        self.conn.commit()
        
        frais_id = self.cursor.lastrowid
        student = self.get_student(student_id)
        type_inscription = student[6] # statut de l'étudiant 
        
        echeances = self.generate_echeancier(frais_id, total_apres_bourse, type_inscription, mode_paiement)
        
        for echeance in echeances:
            self.cursor.execute('''
                INSERT INTO echeancier (frais_id, mois, montant, paye, type)
                VALUES (?, ?, ?, ?, ?)
            ''', echeance)
        
        self.conn.commit()
        return frais_id
    
    # Méthode pour les informations de l'école
    def add_school_info(self, school_info):
        self.cursor.execute('''
            INSERT INTO school_info (school_name, phone_number, email, director_name, signature)
            VALUES (?, ?, ?, ?, ?)
        ''', school_info)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_school_info(self):
        self.cursor.execute('SELECT * FROM school_info WHERE id = 1')
        return self.cursor.fetchone()

    def update_school_info(self, school_info):
        self.cursor.execute('''
            UPDATE school_info
            SET school_name=?, phone_number=?, email=?, director_name=?, signature=?
            WHERE id=1
        ''', school_info)
        self.conn.commit()
    
    # Méthode pour remplir la base de données avec des données de test
    def populate_test_data(self):
        print("Populating test data...")
        # Ajouter des enseignants
        teacher1_id = self.add_teacher(('Dupont', 'Jean', 'jean.dupont@example.com', '0102030405'))
        teacher2_id = self.add_teacher(('Martin', 'Marie', 'marie.martin@example.com', '0607080910'))
        teacher3_id = self.add_teacher(('Lefebvre', 'Sophie', 'sophie.lefebvre@example.com', '0708091011'))

        # Ajouter des classes
        class1_id = self.add_class(('CP', teacher1_id))
        class2_id = self.add_class(('CE1', teacher2_id))
        class3_id = self.add_class(('CE2', teacher3_id))

        stud_1 = self.add_student(('Durand', 'Paul', '2017-05-15', 'Française', 'M', 'Inscription', class1_id))
        stud_2 = self.add_student(('Leroy', 'Sophie', '2016-08-22', 'Française', 'F', 'Réinscription', class2_id))
        stud_3 = self.add_student(('Mbongo', 'Jean', '2015-03-10', 'Gabonaise', 'M', 'Inscription', class3_id))
        stud_4 = self.add_student(('Smith', 'Emma', '2016-11-30', 'Américaine', 'F', 'Inscription', class2_id))
        stud_5 = self.add_student(('Dubois', 'Lucas', '2015-07-05', 'Française', 'M', 'Réinscription', class3_id))

        # Ajouter des responsables
        
        resp_1 = self.add_responsable(('Père', 'Durand', 'Pierre', '0101010101', '0202020202', 'pierre.durand@example.com'))
        resp_2 = self.add_responsable(('Mère', 'Durand', 'Marie', '0303030303', '0404040404', 'marie.durand@example.com'))
        resp_3 = self.add_responsable(('Mère', 'Leroy', 'Claire', '0505050505', '0606060606', 'claire.leroy@example.com'))
        resp_4 = self.add_responsable(('Père', 'Mbongo', 'Robert', '0707070707', '0808080808', 'robert.mbongo@example.com'))
        resp_5 = self.add_responsable(('Mère', 'Smith', 'Sarah', '0909090909', '1010101010', 'sarah.smith@example.com'))
        resp_6 = self.add_responsable(('Père', 'Dubois', 'Thomas', '1111111111', '1212121212', 'thomas.dubois@example.com'))
        resp_7 = self.add_responsable(('Tuteur', 'Martin', 'Paul', '1313131313', '1414141414', 'paul.martin@example.com'))
    

        # Lier étudiants et responsables
        self.link_student_responsable(stud_1, resp_1)
        self.link_student_responsable(stud_1, resp_2)
        self.link_student_responsable(stud_2, resp_3)
        self.link_student_responsable(stud_3, resp_4)
        self.link_student_responsable(stud_4, resp_5)
        self.link_student_responsable(stud_5, resp_6)
        self.link_student_responsable(stud_5, resp_7)

        # Ajouter des frais de scolarité avec différents modes de paiement et bourses
        self.add_frais_scolarite(stud_1, 'standard', 10)  # Inscription, bourse 10%
        self.add_frais_scolarite(stud_2, 'echéancier', 0)  # Réinscription, pas de bourse
        self.add_frais_scolarite(stud_3, 'standard', 20)  # Inscription, bourse 20%
        self.add_frais_scolarite(stud_4, 'echéancier', 5)  # Inscription, bourse 5%
        self.add_frais_scolarite(stud_5, 'standard', 0)  # Réinscription, pas de bourse

    def __del__(self):
        self.conn.close()