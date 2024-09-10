import sqlite3

class DatabaseManager:
    def __init__(self, db_path, verbose=True):
        self.db_path = db_path
        self.conn = None
        self.verbose = verbose

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            if self.verbose:
                print("Connection to SQLite DB successful")
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")

    def reset_database(self):
        if self.conn is None:
            if self.verbose:
                print("Error! Cannot create the database connection.")
            return

        cur = self.conn.cursor()
        try:
            # Получение списка всех таблиц
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cur.fetchall()

            # Сброс всех таблиц в дефолтное значение
            for table in tables:
                table_name = table[0]
                cur.execute(f"DELETE FROM {table_name};")
                cur.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table_name}';")

            self.conn.commit()
            if self.verbose:
                print("Database reset successfully")
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")
        finally:
            cur.close()

    def read_data(self):
        if self.conn is None:
            if self.verbose:
                print("Error! Cannot create the database connection.")
            return

        cur = self.conn.cursor()
        try:
            # Выполнение запроса для чтения данных из таблицы
            cur.execute("SELECT * FROM myapp_settings")
            rows = cur.fetchall()
            data = {}
            for row in rows:
                data = {
                    'drink1': row[1],
                    'drink2': row[2],
                    'status': row[3],
                    'todo1': row[4],
                    'todo2': row[5]
                }

            if self.verbose:
                print(data)
            return data
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")
        finally:
            cur.close()

    
    def read_single_value(self, key):
        if self.conn is None:
            if self.verbose:
                print("Error! Cannot create the database connection.")
            return

        cur = self.conn.cursor()
        try:
            # Выполнение запроса для чтения одного значения из таблицы
            cur.execute(f"SELECT {key} FROM myapp_settings")
            value = cur.fetchone()
            if value:
                value = value[0]
            else:
                value = None

            if self.verbose:
                print(f"Read single value: key={key}, value={value}")
            return value
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")
        finally:
            cur.close()
            

    def update_data(self, key, new_value):
        if self.conn is None:
            if self.verbose:
                print("Error! Cannot create the database connection.")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(f"UPDATE myapp_settings SET {key} = ?", (new_value,))
            self.conn.commit()
            if self.verbose:
                print(f"Data updated successfully: key={key}, new_value={new_value}")
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")
        finally:
            cur.close()

    def insert_data(self, key, value):
        if self.conn is None:
            if self.verbose:
                print("Error! Cannot create the database connection.")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(f"INSERT INTO myapp_settings ({key}) VALUES (?)", (value,))
            self.conn.commit()
            if self.verbose:
                print(f"Data inserted successfully: key={key}, value={value}")
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")
        finally:
            cur.close()

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            if self.verbose:
                print("Connection closed")

def main():
    db_manager = DatabaseManager('path/to/your/database.db', verbose=True)
    db_manager.create_connection()
    db_manager.reset_database()
    data = db_manager.read_data()
    print(data)
    db_manager.update_data('drink1', 10)
    db_manager.close_connection()

if __name__ == "__main__":
    main()