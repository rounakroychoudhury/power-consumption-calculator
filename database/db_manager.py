"""
Database Manager Module
Handles all database operations for storing and retrieving calculation history.
"""

import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    """
    A class to manage SQLite database operations for the Power Calculator.
    """
    
    def __init__(self, db_path='instance/calculator.db'):
        """
        Initialize the database manager.
        
        Parameters:
        - db_path: Path where the database file will be stored
        """
        self.db_path = db_path
        
        # Create the instance folder if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Create the database and table when initialized
        self.create_table()
    
    def create_table(self):
        """
        Create the 'calculations' table if it doesn't exist.
        
        Table structure:
        - id: Unique identifier for each calculation
        - circuit_type: Type of circuit (Single-Phase AC, Three-Phase AC, DC)
        - voltage: Input voltage value
        - current: Input current value
        - power_factor: Input power factor
        - duration: Input duration in hours
        - real_power_w: Calculated real power in watts
        - real_power_kw: Calculated real power in kilowatts
        - reactive_power_var: Calculated reactive power in VAR
        - reactive_power_kvar: Calculated reactive power in kVAR
        - apparent_power_va: Calculated apparent power in VA
        - apparent_power_kva: Calculated apparent power in kVA
        - energy_wh: Calculated energy in Wh
        - energy_kwh: Calculated energy in kWh
        - timestamp: When the calculation was made
        """
        
        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create the table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS calculations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    circuit_type TEXT NOT NULL,
                    voltage REAL NOT NULL,
                    current REAL NOT NULL,
                    power_factor REAL NOT NULL,
                    duration REAL NOT NULL,
                    real_power_w REAL NOT NULL,
                    real_power_kw REAL NOT NULL,
                    reactive_power_var REAL NOT NULL,
                    reactive_power_kvar REAL NOT NULL,
                    apparent_power_va REAL NOT NULL,
                    apparent_power_kva REAL NOT NULL,
                    energy_wh REAL NOT NULL,
                    energy_kwh REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            
            print("✓ Database table created/verified successfully")
            
        except sqlite3.Error as e:
            print(f"✗ Database error: {e}")
            raise
    
    def save_calculation(self, result):
        """
        Save a calculation result to the database.
        
        Parameters:
        - result: Dictionary with calculation results from PowerCalculator
        
        Returns:
        - ID of the saved calculation
        """
        
        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert the calculation result into the table
            cursor.execute('''
                INSERT INTO calculations (
                    circuit_type, voltage, current, power_factor, duration,
                    real_power_w, real_power_kw, reactive_power_var, reactive_power_kvar,
                    apparent_power_va, apparent_power_kva, energy_wh, energy_kwh
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result['circuit_type'],
                result['voltage'],
                result['current'],
                result['power_factor'],
                result['duration'],
                result['real_power_w'],
                result['real_power_kw'],
                result['reactive_power_var'],
                result['reactive_power_kvar'],
                result['apparent_power_va'],
                result['apparent_power_kva'],
                result['energy_wh'],
                result['energy_kwh']
            ))
            
            # Get the ID of the inserted row
            calculation_id = cursor.lastrowid
            
            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            
            print(f"✓ Calculation saved with ID: {calculation_id}")
            return calculation_id
            
        except sqlite3.Error as e:
            print(f"✗ Error saving calculation: {e}")
            raise
    
    def get_all_calculations(self):
        """
        Retrieve all calculations from the database.
        
        Returns:
        - List of dictionaries, each containing one calculation record
        """
        
        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_path)
            
            # This makes the results behave like dictionaries
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Fetch all calculations, ordered by most recent first
            cursor.execute('SELECT * FROM calculations ORDER BY timestamp DESC')
            rows = cursor.fetchall()
            
            # Convert rows to list of dictionaries
            calculations = [dict(row) for row in rows]
            
            conn.close()
            
            return calculations
            
        except sqlite3.Error as e:
            print(f"✗ Error retrieving calculations: {e}")
            return []
    
    def get_calculation_by_id(self, calc_id):
        """
        Retrieve a specific calculation by its ID.
        
        Parameters:
        - calc_id: ID of the calculation to retrieve
        
        Returns:
        - Dictionary containing the calculation record, or None if not found
        """
        
        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Fetch the specific calculation
            cursor.execute('SELECT * FROM calculations WHERE id = ?', (calc_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            # Return as dictionary if found, None otherwise
            return dict(row) if row else None
            
        except sqlite3.Error as e:
            print(f"✗ Error retrieving calculation: {e}")
            return None
    
    def delete_calculation(self, calc_id):
        """
        Delete a specific calculation from the database.
        
        Parameters:
        - calc_id: ID of the calculation to delete
        
        Returns:
        - True if successful, False otherwise
        """
        
        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete the calculation
            cursor.execute('DELETE FROM calculations WHERE id = ?', (calc_id,))
            
            # Commit the changes
            conn.commit()
            conn.close()
            
            print(f"✓ Calculation {calc_id} deleted successfully")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Error deleting calculation: {e}")
            return False
    
    def clear_all_calculations(self):
        """
        Delete all calculations from the database.
        
        Returns:
        - True if successful, False otherwise
        """
        
        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete all records
            cursor.execute('DELETE FROM calculations')
            
            # Commit the changes
            conn.commit()
            conn.close()
            
            print("✓ All calculations cleared successfully")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Error clearing calculations: {e}")
            return False
    
    def get_statistics(self):
        """
        Get basic statistics about the calculations.
        
        Returns:
        - Dictionary with stats (total count, average power, etc.)
        """
        
        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get statistics
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_calculations,
                    AVG(real_power_kw) as avg_power_kw,
                    MAX(real_power_kw) as max_power_kw,
                    MIN(real_power_kw) as min_power_kw,
                    SUM(energy_kwh) as total_energy_kwh
                FROM calculations
            ''')
            
            row = cursor.fetchone()
            conn.close()
            
            # Return stats as dictionary
            return {
                'total_calculations': row[0] if row[0] else 0,
                'avg_power_kw': round(row[1], 2) if row[1] else 0,
                'max_power_kw': round(row[2], 2) if row[2] else 0,
                'min_power_kw': round(row[3], 2) if row[3] else 0,
                'total_energy_kwh': round(row[4], 2) if row[4] else 0
            }
            
        except sqlite3.Error as e:
            print(f"✗ Error getting statistics: {e}")
            return {}