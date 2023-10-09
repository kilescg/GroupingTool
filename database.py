import sqlite3
from sqlite3 import Error
import random
from utils import *


class SDE_SQLLite:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.connect_db()

    def connect_db(self):
        """Connect to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
        except Error as e:
            raise Exception(f"Error connecting to the database: {e}")

    def execute_query(self, query, values=None):
        """Execute a SQL query with optional values."""
        try:
            cursor = self.conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            self.conn.rollback()
            raise Exception(f"Error executing SQL query: {e}")

    def insert_data(self, table_name, data):
        """Insert data into a table."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        status = self.execute_query(query, tuple(data.values()))
        self.conn.commit()
        return status

    def search_value(self, table_name, column_name, keyword, limit=100):
        """search data from a table and column."""
        cursor = self.conn.cursor()
        query = f"SELECT {column_name} FROM {table_name} WHERE {column_name} LIKE ? LIMIT {limit}"
        keyword_with_wildcard = f"%{keyword}%"
        cursor.execute(query, (keyword_with_wildcard,))
        results = cursor.fetchall()
        return results

    def select_data(self, table_name, columns=None, where_condition=None):
        """Select data from a table."""
        if columns is None:
            column_names = "*"
        else:
            column_names = ', '.join(columns)
        query = f"SELECT {column_names} FROM {table_name}"
        if where_condition:
            query += f" WHERE {where_condition}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def close_db(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()


def generate_mock_data():
    from faker import Faker

    fake = Faker()
    db_manager = SDE_SQLLite("database/DB_sdeautodeploy.db")

    '''
    Solution
    '''
    for i in range(10):
        solution = {
            'solution_id': f'{i}',
            'solution_name': fake.first_name(),
        }
        db_manager.insert_data('solution', solution)

    '''
    Project
    '''
    project_num = 0
    for i in range(10):
        for _ in range(random.randint(0, 4)):
            project = {
                'project_id': f'{project_num}',
                'dev_id': 1,
                'project_name': fake.last_name(),
                'datetime': get_date_time()
            }
            project_num += 1
            db_manager.insert_data('project', project)

    '''
    Device Configuration
    '''
    device_config_num = 0
    for i in range(project_num):
        for _ in range(random.randint(0, 4)):
            device_config_id = {
                'device_configuration_id': f'{device_config_num}',
                'device_name_prefix': f'{random.randint(1,99)}_{random.randint(1,99)}',
                'project_id': f'{i}',
                'devicetype_id': f'{random.randint(0,38)}',
                'controllertype_id': f'{random.randint(0,24)}',
                'emplacement_id': f'{random.randint(0,2)}',
                'room': f'room{random.randint(1,99)}',
            }
            device_config_num += 1
            db_manager.insert_data('device_configuration', device_config_id)


if __name__ == '__main__':

    generate_mock_data()
    # insert types json to database
    '''
    db = SDE_SQLLite("database/DB_sdeautodeploy.db")
    with open('configuration.json') as f:
        data = json.load(f)
        for idx, val in enumerate(data["location"]):
            dt = get_date_time()
            template_data = (idx, val, dt)
            db.insert_emplacement_type(template_data)
        for idx, val in enumerate(data["controller_type"]):
            dt = get_date_time()
            template_data = (idx, val, dt)
            db.insert_controller_type(template_data)
        for idx, val in enumerate(data["device_type"]):
            dt = get_date_time()
            template_data = (idx, val, dt)
            db.insert_device_type(template_data)
    '''

    # insert dummy child to database
    # mac_id,status,note,print_label,datetime
    # fake = Faker()
    # db = SDE_SQLLite("database/DB_sdeautodeploy.db")
    # with open('configuration.json') as f:
    #     data = json.load(f)
    #     for num in range(999):
    #         dt = get_date_time()
    #         note = ''
    #         status = 'good' if random.random() > 0.5 else 'ng'
    #         if (status == 'good'):
    #             note = ''
    #         if (status == 'ng'):
    #             note = 'controller broke'
    #         template_data = (f'mac{num}', status, note, '1', dt)
    #         db.insert_device_incoming(template_data)
    #         print(num)

    # insert dummy edge to database
    # fake = Faker()
    # generate = DocumentGenerator()
    # db = SDE_SQLLite("database/DB_sdeautodeploy.db")
    # with open('configuration.json') as f:
    #     data = json.load(f)
    #     for num in range(999):
    #         dt = get_date_time()
    #         note_txt = fake.address()
    #         template_data = (num, note_txt)
    #         db.insert_note(template_data)
    #         print(num)

    # incser dummy notes to database
    # fake = Faker()
    # db = SDE_SQLLite("database/DB_sdeautodeploy.db")
    # for num in range(999):
    #     dt = get_date_time()
    #     template_data = (num, f"fame_{num}", num)
    #     db.insert_edge_device(template_data)
    #     print(num)
