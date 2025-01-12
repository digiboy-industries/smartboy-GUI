import sqlite3
import os
from datetime import datetime

def save_to_db(temp):
    """
    temp is dictionary
    """
    today_date = datetime.now().strftime("%Y-%m-%d")
    db_name = f"{today_date}.db"

    # Check if the database exists, create if it doesn't
    if not os.path.exists(db_name):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            # Create a table for storing the data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT NOT NULL,
                    XRPM_name TEXT,
                    XRPM INTEGER,
                    S1_name TEXT,
                    S1_value REAL,
                    S1_unit TEXT,
                    S1_current REAL,
                    S1_voltage REAL,

                    S2_name TEXT,
                    S2_value REAL,
                    S2_unit TEXT,
                    S2_current REAL,
                    S2_voltage REAL,
                    
                    S3_name TEXT,
                    S3_value REAL,
                    S3_unit TEXT,
                    S3_current REAL,
                    S3_voltage REAL,
                    
                    S4_name TEXT,
                    S4_value REAL,
                    S4_unit TEXT,
                    S4_current REAL,
                    S4_voltage REAL,
                           
                    S5_name TEXT,
                    S5_value REAL,
                    S5_unit TEXT,
                    S5_current REAL,
                    S5_voltage REAL,
                           
                    S6_name TEXT,
                    S6_value REAL,
                    S6_unit TEXT,
                    S6_current REAL,
                    S6_voltage REAL,

                    S7_name TEXT,
                    S7_value REAL,
                    S7_unit TEXT,
                    S7_current REAL,
                    S7_voltage REAL,
                    S8_current REAL,
                    S8_voltage REAL
                )
            ''')
            conn.commit()

    # Insert data into the database
    if (temp != ""):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Extracting values from the data dictionary
            XRPM = temp.get('XRPM', {})
            S1_current = temp.get('S1', {}).get('current', None)
            S1_voltage = temp.get('S1', {}).get('voltage', None)
            S2_current = temp.get('S2', {}).get('current', None)
            S2_voltage = temp.get('S2', {}).get('voltage', None)
            S3_current = temp.get('S3', {}).get('current', None)
            S3_voltage = temp.get('S3', {}).get('voltage', None)
            S4_current = temp.get('S4', {}).get('current', None)
            S4_voltage = temp.get('S4', {}).get('voltage', None)

            # Insert data into the table
            cursor.execute('''
                INSERT INTO measurements (datetime, XRPM, S1_current, S1_voltage, S2_current, S2_voltage, S3_current, S3_voltage, S4_current, S4_voltage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (now, XRPM, S1_current, S1_voltage, S2_current, S2_voltage, S3_current, S3_voltage, S4_current, S4_voltage))
            conn.commit()