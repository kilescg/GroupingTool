import mysql.connector
import json
from utils import *


class MySQLHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def insert_data(self, table_name, data_dict):
        if not self.connection:
            self.connect()

        # Create placeholders for column names and values
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['%s'] * len(data_dict))

        # Build the INSERT query dynamically
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        # Extract the values from the dictionary
        data = tuple(data_dict.values())

        self.cursor.execute(insert_query, data)
        self.connection.commit()

    def select_data(self, table_name, column_name=[], condition=None):
        if not self.connection:
            self.connect()

        selected_column = ''

        if column_name == []:
            selected_column = '*'
        else:
            selected_column = ', '.join(column_name)

        select_query = f"SELECT {selected_column} FROM {table_name}"
        if condition != None:
            select_query += f' WHERE {condition}'
        self.cursor.execute(select_query)
        results = self.cursor.fetchall()
        return results

    def get_data_with_keyword(self, table_name, column_name, keyword, limit=100):
        try:
            # Define the SQL query to retrieve data
            query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE %s LIMIT %s"

            # Execute the query
            self.cursor.execute(query, (f"%{keyword}%", limit))

            # Fetch the results
            result = self.cursor.fetchall()

            return result

        except mysql.connector.Error as error:
            print(f"Error: {error}")
            return []

    def execute_query(self, query, params=None):
        try:
            # Create a cursor to execute SQL queries
            cursor = self.connection.cursor()

            # Execute the query with optional parameters
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Commit changes (if needed) and fetch results (if applicable)
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = None
            return result
        except mysql.connector.Error as error:
            print(f"Error: {error}")
            return []

    def search_value(self, table_name, column_name, keyword):
        cursor = self.connection.cursor()

        # Create a query to search for names in the specified column using the keyword
        query = f"SELECT {column_name} FROM {table_name} WHERE {column_name} LIKE %s LIMIT 100"

        # Add a '%' wildcard before and after the keyword to perform a partial match
        keyword_with_wildcard = f"%{keyword}%"

        # Execute the query with the keyword
        cursor.execute(query, (keyword_with_wildcard,))

        # Fetch all the matching results
        results = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        return results

    def close(self):
        self.disconnect()

    def update_value(self, table_name, column_name, new_value, condition, params=None):
        if not self.connection:
            self.connect()

        try:
            # Create a SQL query to update the value in the specified column based on a condition
            query = f"UPDATE {table_name} SET {column_name} = %s WHERE {condition}"

            # Execute the query with the new value and optional parameters
            if params:
                self.cursor.execute(query, (new_value,) + params)
            else:
                self.cursor.execute(query, (new_value,))

            # Commit the changes
            self.connection.commit()

        except mysql.connector.Error as error:
            print(f"Error: {error}")


def add_types_dummy():
    from faker import Faker
    import random

    with open('./configuration.json') as f:
        data = json.load(f)
        for idx, val in enumerate(data["location"]):
            dt = get_date_time()
            field_name = ['emplacement_name', 'datetime']
            template_data = [val, dt]
            input_data = dict(zip(field_name, template_data))
            db_handle.insert_data('emplacement_type', input_data)
        for idx, val in enumerate(data["controller_type"]):
            dt = get_date_time()
            field_name = ['controller_type_name', 'datetime']
            template_data = [val, dt]
            input_data = dict(zip(field_name, template_data))
            db_handle.insert_data('controller_type', input_data)
        for idx, val in enumerate(data["device_type"]):
            dt = get_date_time()
            field_name = ['device_type_name', 'datetime']
            template_data = [val, dt]
            input_data = dict(zip(field_name, template_data))
            db_handle.insert_data('device_type', input_data)

        fake = Faker()
        for i in range(100):
            field_name = ['note_detail']
            template_data = [fake.address()]
            input_data = dict(zip(field_name, template_data))

        for i in range(100):
            field_name = ['port_no', 'ip_address', 'edge_id', 'edgetype_id', 'package_id', 'thingsgroup_id',
                          'tuyauniq_id', 'note_id', 'label_print', 'thinggroup_add', 'status', 'datatime_start', 'datatime_end']
            template_data = [i, fake.ipv4_private(), random_string(
                12), i, i, i, i, i, '1', '1', '1', fake.date_time(), fake.date_time()]
            input_data = dict(zip(field_name, template_data))
            db_handle.insert_data('edge_device', input_data)

        for i in range(100):
            field_name = ['child_id', 'bom_id',
                          'print_label', 'note', 'datetime']
            template_data = [random_string(
                12), 0, '0', fake.address(), fake.date_time()]
            input_data = dict(zip(field_name, template_data))
            db_handle.insert_data('child_device', input_data)


db_host = "localhost"
db_user = "root"
db_password = "password"
db_name = "db_sde"

db_handle = MySQLHandler(db_host, db_user, db_password, db_name)
db_handle.connect()

if __name__ == '__main__':
    add_types_dummy()
