import sqlite3
from datetime import datetime


# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a table for a specific month_year
def create_table(conn, month_year):
    sql = f'''CREATE TABLE IF NOT EXISTS {month_year} (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                details TEXT,
                p_s TEXT CHECK (p_s IN ('p', 's')),
                amount INTEGER
            );'''
    try:
        c = conn.cursor()
        c.execute(sql)
    except sqlite3.Error as e:
        print(e)

# Function to insert data into the table
def insert_data(conn, month_year, date, details, p_s, amount):
    sql = f'''INSERT INTO {month_year} (date, details, p_s, amount)
                VALUES (?, ?, ?, ?);'''
    try:
        c = conn.cursor()
        c.execute(sql, (date, details, p_s, amount))
        conn.commit()
        return c.lastrowid
    except sqlite3.Error as e:
        print(e)
        return None

# Function to fetch data from the table
def fetch_data(conn, month_year):
    sql = f'SELECT * FROM {month_year};'
    try:
        c = conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        return rows
    except sqlite3.Error as e:
        print(e)
        return None

# Function to update data in the table
def update_data(conn, month_year, uid, date, details, p_s, amount):
    sql = f'''UPDATE {month_year}
                SET date = ?,
                details = ?,
                p_s = ?,
                amount = ?
                WHERE uid = ?;'''
    try:
        c = conn.cursor()
        c.execute(sql, (date, details, p_s, amount, uid))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Function to delete data from the table
def delete_data(conn, month_year, uid):
    sql = f'DELETE FROM {month_year} WHERE uid = ?;'
    try:
        c = conn.cursor()
        c.execute(sql, (uid,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)




# Function to fetch available tables in the database
def get_available_tables(db_file):
    conn = create_connection(db_file)
    try:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        conn.close()
        return [table[0] for table in tables]
    except sqlite3.Error as e:
        print(e)
        return []

# Function to fetch purchase and sales totals for a given table
def get_purchase_sales_totals(db_file, table_name):
    conn = create_connection(db_file)
    try:
        c = conn.cursor()
        c.execute(f"SELECT SUM(CASE WHEN p_s='P' THEN amount ELSE 0 END), SUM(CASE WHEN p_s='S' THEN amount ELSE 0 END) FROM {table_name};")
        totals = c.fetchone()
        conn.close()
        return totals
    except sqlite3.Error as e:
        print(e)
        return (0, 0)  # Default values if there's an error

# Function to fetch data from a specific table
def fetch_data(db_file, table_name):
    conn = create_connection(db_file)
    try:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name};")
        rows = c.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(e)
        return []








# Usage example:
if __name__ == '__main__':
    db_file = 'my_database.db'  # Replace with your database file name
    conn = create_connection(db_file)
    if conn is not None:
        current_month_year = datetime.now().strftime('%B_%Y')  # Get current month and year as text
        create_table(conn, current_month_year)
        
        # Inserting data
        # insert_data(conn, current_month_year, '2023-12-25', 'Sample details', 'p', 500)
        
        # Fetching and printing data
        # rows = fetch_data(conn, current_month_year)
        # if rows:
        #     for row in rows:
        #         print(row)
        
        # # Updating data
        # update_data(conn, current_month_year, 1, '2023-12-25', 'Updated details', 's', 750)
        
        # # Deleting data
        # delete_data(conn, current_month_year, 1)
        
        conn.close()
    else:
        print('Connection to database failed.')
