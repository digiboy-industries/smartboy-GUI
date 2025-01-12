import sqlite3
import os
from datetime import datetime

def save_to_db(Sdictionary):
    """
    Sdictionary is dictionary after parsed from sensor
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
                    Sensor_RPM INTEGER,
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
                    
                    S8_name TEXT,
                    S8_value REAL,
                    S8_unit TEXT,
                    S8_current REAL,
                    S8_voltage REAL
                )
            ''')
            conn.commit()

    # Insert data into the database
    if (Sdictionary != {} and type(Sdictionary)== dict):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Extracting values from the data dictionary
            XRPM = Sdictionary.get('XRPM', {})
            S1_current = Sdictionary.get('S1', {}).get('current', None)
            S1_voltage = Sdictionary.get('S1', {}).get('voltage', None)
            S1_name = Sdictionary.get('S1', {}).get('name', None)
            S1_value = Sdictionary.get('S1', {}).get('value', None)
            S1_unit = Sdictionary.get('S1', {}).get('unit', None)

            S2_current = Sdictionary.get('S2', {}).get('current', None)
            S2_voltage = Sdictionary.get('S2', {}).get('voltage', None)
            S2_name = Sdictionary.get('S2', {}).get('name', None)
            S2_value = Sdictionary.get('S2', {}).get('value', None)
            S2_unit = Sdictionary.get('S2', {}).get('unit', None)

            S3_current = Sdictionary.get('S3', {}).get('current', None)
            S3_voltage = Sdictionary.get('S3', {}).get('voltage', None)
            S3_name = Sdictionary.get('S3', {}).get('name', None)
            S3_value = Sdictionary.get('S3', {}).get('value', None)
            S3_unit = Sdictionary.get('S3', {}).get('unit', None)

            S4_current = Sdictionary.get('S4', {}).get('current', None)
            S4_voltage = Sdictionary.get('S4', {}).get('voltage', None)
            S4_name = Sdictionary.get('S4', {}).get('name', None)
            S4_value = Sdictionary.get('S4', {}).get('value', None)
            S4_unit = Sdictionary.get('S4', {}).get('unit', None)

            S5_current = Sdictionary.get('S5', {}).get('current', None)
            S5_voltage = Sdictionary.get('S5', {}).get('voltage', None)
            S5_name = Sdictionary.get('S5', {}).get('name', None)
            S5_value = Sdictionary.get('S5', {}).get('value', None)
            S5_unit = Sdictionary.get('S5', {}).get('unit', None)

            S6_current = Sdictionary.get('S6', {}).get('current', None)
            S6_voltage = Sdictionary.get('S6', {}).get('voltage', None)
            S6_name = Sdictionary.get('S6', {}).get('name', None)
            S6_value = Sdictionary.get('S6', {}).get('value', None)
            S6_unit = Sdictionary.get('S6', {}).get('unit', None)

            S7_current = Sdictionary.get('S7', {}).get('current', None)
            S7_voltage = Sdictionary.get('S7', {}).get('voltage', None)
            S7_name = Sdictionary.get('S7', {}).get('name', None)
            S7_value = Sdictionary.get('S7', {}).get('value', None)
            S7_unit = Sdictionary.get('S7', {}).get('unit', None)

            S8_current = Sdictionary.get('S8', {}).get('current', None)
            S8_voltage = Sdictionary.get('S8', {}).get('voltage', None)
            S8_name = Sdictionary.get('S8', {}).get('name', None)
            S8_value = Sdictionary.get('S8', {}).get('value', None)
            S8_unit = Sdictionary.get('S8', {}).get('unit', None)
            # Insert data into the table
            cursor.execute('''
                INSERT INTO measurements (datetime, Sensor_RPM, S1_name, S1_value, S1_unit, S1_current, S1_voltage, 
                S2_name, S2_value, S2_unit, S2_current, S2_voltage, 
                S3_name, S3_value, S3_unit, S3_current, S3_voltage, 
                S4_name, S4_value, S4_unit, S4_current, S4_voltage,
                S5_name, S5_value, S5_unit, S5_current, S5_voltage,
                S6_name, S6_value, S6_unit, S6_current, S6_voltage,
                S7_name, S7_value, S7_unit, S7_current, S7_voltage,
                S8_name, S8_value, S8_unit, S8_current, S8_voltage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? , ?,
                        ?, ?, ?, ?, ?, ?, ?, ?, ? , ?,
                        ?, ?, ?, ?, ?, ?, ?, ?, ? , ?,
                        ?, ?, ?, ?, ?, ?, ?, ?, ? , ?,
                        ?, ?)
            ''', (now, XRPM, S1_name, S1_value, S1_unit, S1_current, S1_voltage,
                  S2_name, S2_value, S2_unit, S2_current, S2_voltage,
                  S3_name, S3_value, S3_unit, S3_current, S3_voltage,
                  S4_name, S4_value, S4_unit, S4_current, S4_voltage,
                  S5_name, S5_value, S5_unit, S5_current, S5_voltage,
                  S6_name, S6_value, S6_unit, S6_current, S6_voltage,
                  S7_name, S7_value, S7_unit, S7_current, S7_voltage,
                  S8_name, S8_value, S8_unit, S8_current, S8_voltage)
                        )
            conn.commit()
            return 0
    else:
        return 1