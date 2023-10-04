import sqlite3
import json
from utils import get_date_time
from sqlite3 import Error
from essential_generators import DocumentGenerator


class SDE_SQLLite():
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.connect_db()

    def connect_db(self):
        '''connect to database'''
        try:
            self.conn = sqlite3.connect(self.db_path)
            return True
        except Error as e:
            print(e)
            return False

    def check_data_exists(self, table_name, column, data):
        # Connect to the SQLite database
        cursor = self.conn.cursor()

        # Create a query to check if data exists in the specified column
        query = f"SELECT COUNT(*) FROM {table_name} WHERE {column} = ?"

        # Execute the query with the provided data value
        cursor.execute(query, (data,))
        result = cursor.fetchone()

        # Check if the count is greater than zero, indicating the data exists
        if result[0] > 0:
            return True
        else:
            return False

    def get_data_from_column(self, table_name, column_name):
        # Connect to the SQLite database
        cursor = self.conn.cursor()

        # Create a query to select data from the specified column
        query = f"SELECT {column_name} FROM {table_name}"

        # Execute the query and fetch all the results
        cursor.execute(query)
        data_list = [row[0] for row in cursor.fetchall()]
        return data_list

    def create_child_device(self, child_device):
        sql = ''' INSERT INTO child_device(child_id,devicetype_id,controllertype_id,emplacement_id,     print_label,datetime) VALUES(?,?,?,?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, child_device)
        self.conn.commit()
        return cur.lastrowid

    def insert_device_type(self, device_type):
        sql = ''' INSERT INTO device_type(devicetype_id,devicetype_name,datetime) VALUES(?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, device_type)
        self.conn.commit()
        return cur.lastrowid

    def insert_controller_type(self, controller_type):
        sql = ''' INSERT INTO controller_type(controllertype_id,controllertype_name,datetime) VALUES(?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, controller_type)
        self.conn.commit()
        return cur.lastrowid

    def insert_emplacement_type(self, emplacement_type):
        sql = ''' INSERT INTO emplacement_type(emplacement_id,emplacement_name,datetime) VALUES(?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, emplacement_type)
        self.conn.commit()
        return cur.lastrowid

    def insert_device_incoming(self, device_incoming):
        sql = ''' INSERT INTO device_incoming(mac_id,status,note,print_label,datetime) VALUES(?,?,?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, device_incoming)
        self.conn.commit()
        return cur.lastrowid

    # super mock lol
    def insert_edge_device(self, device_incoming):
        sql = ''' INSERT INTO edge_device(no,edge_id,note_id) VALUES(?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, device_incoming)
        self.conn.commit()
        return cur.lastrowid

    def insert_note(self, note):
        sql = ''' INSERT INTO note(note_id, note_detail) VALUES(?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, note)
        self.conn.commit()
        return cur.lastrowid

    def insert_kitting_device(self, kitting_device):
        sql = ''' INSERT INTO kitting_device(edge_id, child_id) VALUES(?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, kitting_device)
        self.conn.commit()
        return cur.lastrowid

    def insert_child_device(self, child_device):
        sql = ''' INSERT INTO child_device(child_id, devicetype_id, controllertype_id, emplacement_id, print_label, datetime) VALUES(?,?,?,?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, child_device)
        self.conn.commit()
        return cur.lastrowid

    def select_from_table(self, table_name, columns=None, where_condition=None):
        # Connect to the SQLite database
        cursor = self.conn.cursor()

        # Create the SELECT statement
        if columns is None:
            column_names = "*"
        else:
            column_names = ", ".join(columns)

        query = f"SELECT {column_names} FROM {table_name}"

        # Add a WHERE clause if a condition is provided
        if where_condition is not None:
            query += f" WHERE {where_condition}"

        # Execute the query
        cursor.execute(query)

        # Fetch all the results
        rows = cursor.fetchall()

        # Get the column names
        column_names = [description[0] for description in cursor.description]

        # Convert the results to a list of dictionaries
        result = []
        for row in rows:
            row_dict = {}
            for i in range(len(column_names)):
                row_dict[column_names[i]] = row[i]
            result.append(row_dict)

        return result

    def select_value_equal(self, table_name, column_name, value1, value2):
        cursor = self.conn.cursor()

        # Create a query to search for values in the specified column using placeholders
        query = f"SELECT {column_name} FROM {table_name} WHERE {value1}='{value2}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def search_value(self, table_name, column_name, keyword):
        cursor = self.conn.cursor()

        # Create a query to search for names in the specified column using the keyword
        query = f"SELECT {column_name} FROM {table_name} WHERE {column_name} LIKE ? LIMIT 100"

        # Add a '%' wildcard before and after the keyword to perform a partial match
        keyword_with_wildcard = f"%{keyword}%"

        # Execute the query with the keyword
        cursor.execute(query, (keyword_with_wildcard,))

        # Fetch all the matching results
        results = cursor.fetchall()

        return results

    def get_note_details_by_edge_id(self, edge_id):
        try:
            # Connect to the SQLite database
            cursor = self.conn.cursor()

            # Execute the SQL query
            cursor.execute("""
                SELECT n.note_detail
                FROM edge_device AS e
                JOIN note AS n ON e.note_id = n.note_id
                WHERE e.edge_id = ?
            """, (edge_id,))

            # Fetch all the results
            note_details = cursor.fetchall()

            return note_details

        except sqlite3.Error as e:
            print("SQLite error:", e)
            return None


if __name__ == '__main__':
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
