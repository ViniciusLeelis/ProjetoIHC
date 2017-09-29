'''
Contém as operações relacionadas ao banco de dados.
'''
import sqlite3
import os

class Database():
    '''
    Class that handles the database operations.
    '''
#cria o banco
    def __init__(self, istest=False):
        '''
        Initialize the database
        '''
        #verifica se tem um banco. Se tiver, ele conecta. Caso contrário, ele cria um.

        database_exists = os.path.isfile('main.db')
        if istest:
            self.connection = sqlite3.connect(
                ':memory:',
                detect_types=sqlite3.PARSE_DECLTYPES,
                check_same_thread=False
            )
        else:
            self.connection = sqlite3.connect(
                'main.db',
                detect_types=sqlite3.PARSE_DECLTYPES,
                check_same_thread=False
            )
        self.cursor = self.connection.cursor()

        if not database_exists or istest:
            self.create_schema()

#cria tres tabelas no banco
    def create_schema(self):
        '''
        Cria o schema do banco de dados caso ele não exista.
        '''
        self.cursor.execute(
            '''
            CREATE TABLE doctors (
                id INTEGER PRIMARY KEY NOT NULL,
                first_name CHAR(40) NOT NULL,
                last_name CHAR(40) NOT NULL,
                telegram_id INT NOT NULL
            )
            '''
        )
        self.cursor.execute(
            '''
            CREATE TABLE patients (
                id INTEGER PRIMARY KEY NOT NULL,
                first_name CHAR(40) NOT NULL,
                last_name CHAR(40) NOT NULL,
                birth_date DATE NOT NULL,
                telegram_id INT NOT NULL
            )
            '''
        )
        self.cursor.execute(
            '''CREATE TABLE appointments (
                id INTEGER PRIMARY KEY NOT NULL,
                date DATETIME NOT NULL,
                address char(200),
                doctor_id INT NOT NULL,
                patient_id INT NOT NULL,
                status INT NOT NULL DEFAULT 0,
                FOREIGN KEY(doctor_id) REFERENCES doctors(id),
                FOREIGN KEY(patient_id) REFERENCES patients(id)
            )
            '''
        )
        self.connection.commit()

    def new_doctor(self, doctor):
        '''
        Creates a new doctor row on the database.
        '''
        args = (
            None,
            doctor['first_name'],
            doctor['last_name'],
            doctor['telegram_id']
        )
        self.cursor.execute(
            '''
            INSERT INTO doctors
            VALUES (?, ?, ?, ?)
            ''', args
        )

#criam entradas nas tabelas
    def new_patient(self, patient):
        '''
        Creates a new patient row on the database.
        '''
        args = (
            None,
            patient['first_name'],
            patient['last_name'],
            patient['birth_date'],
            patient['telegram_id']
        )
        self.cursor.execute(
            '''
            INSERT INTO patients
            VALUES (?, ?, ?, ?, ?)
            ''', args
        )

    def new_appointment(self, appointment):
        '''
        Creates a new appointment row on the database.
        '''
        args = (
            None,
            appointment['when'],
            appointment['address'],
            appointment['doctor_id'],
            appointment['patient_id'],
            appointment['status'] if 'status' in appointment else 0
        )
        self.cursor.execute(
            '''
            INSERT INTO appointments
            VALUES (?, ?, ?, ?, ?, ?)
            ''', args
        )
        self.connection.commit()

#puxa do banco
    def get_doctor(self, doctor_id):
        '''
        Get doctor by its id
        '''
        args = (str(doctor_id))
        self.cursor.execute(
            '''
            SELECT * FROM doctors WHERE id = ?
            ''', args
        )
        record = self.cursor.fetchone()
        return {
            'id' : record[0],
            'first_name' : record[1],
            'last_name' : record[2],
            'telegram_id' : record[3]
        }

    def get_patient(self, patient_id):
        '''
        Get patient by its id
        '''
        args = (str(patient_id))
        self.cursor.execute(
            '''
            SELECT * FROM patients WHERE id = ?
            ''', args
        )
        record = self.cursor.fetchone()
        return {
            'id' : record[0],
            'first_name' : record[1],
            'last_name' : record[2],
            'birth_date' : record[3],
            'telegram_id' : record[4]
        }

    def get_appointments(self, patient_id):
        '''
        Returns all patient's appointments
        '''
        args = (str(patient_id))
        self.cursor.execute(
            '''
            SELECT * FROM appointments WHERE patient_id = ?
            ''', args
        )
        records = [{
            'id' : record[0],
            'date': record[1],
            'address' : record[2],
            'doctor_id' : record[3],
            'patient_id' : record[4],
            'status' : Database.get_appointment_status(record[5])
        } for record in self.cursor.fetchall()]
        return records

    def get_doctors(self):
        '''
        Returns doctors
        '''
        self.cursor.execute(
            '''
            SELECT * FROM doctors LIMIT 5
            '''
        )
        return [{
            'id' : record[0],
            'first_name' : record[1],
            'last_name' : record[2],
            'telegram_id' : record[3]
        } for record in self.cursor.fetchall()]

    @staticmethod
    def get_appointment_status(status: int):
        '''
        Converts the status from integer to string.
        '''
        if status == 0:
            return 'scheduled'
        elif status == 1:
            return 'done'
        return 'canceled'

if __name__ == '__main__':
    Database().create_schema()
