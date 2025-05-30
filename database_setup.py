import sqlite3
import pandas as pd
from datetime import datetime
from config import DATABASE_NAME
from data_extraction import NASADataExtractor

class DatabaseManager:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Create asteroids and close_approach tables"""
        cursor = self.connect()
        
        # Create asteroids table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asteroids (
                id INTEGER,
                name TEXT,
                absolute_magnitude_h REAL,
                estimated_diameter_min_km REAL,
                estimated_diameter_max_km REAL,
                is_potentially_hazardous_asteroid BOOLEAN
            )
        ''')
        
        # Create close_approach table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS close_approach (
                neo_reference_id INTEGER,
                close_approach_date DATE,
                relative_velocity_kmph REAL,
                astronomical REAL,
                miss_distance_km REAL,
                miss_distance_lunar REAL,
                orbiting_body TEXT
            )
        ''')
        
        self.conn.commit()
        print("Tables created successfully!")
    
    def insert_data(self, asteroid_data, approach_data):
        """Insert data into tables"""
        cursor = self.connect()
        
        # Insert asteroid data
        for asteroid in asteroid_data:
            cursor.execute('''
                INSERT INTO asteroids VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                asteroid['id'],
                asteroid['name'],
                asteroid['absolute_magnitude_h'],
                asteroid['estimated_diameter_min_km'],
                asteroid['estimated_diameter_max_km'],
                asteroid['is_potentially_hazardous_asteroid']
            ))
        
        # Insert approach data
        for approach in approach_data:
            cursor.execute('''
                INSERT INTO close_approach VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                approach['neo_reference_id'],
                approach['close_approach_date'],
                approach['relative_velocity_kmph'],
                approach['astronomical'],
                approach['miss_distance_km'],
                approach['miss_distance_lunar'],
                approach['orbiting_body']
            ))
        
        self.conn.commit()
        print(f"Inserted {len(asteroid_data)} asteroid records")
        print(f"Inserted {len(approach_data)} approach records")
    
    def setup_database(self):
        """Complete database setup process"""
        print("Setting up database...")
        
        # Create tables
        self.create_tables()
        
        # Extract data
        extractor = NASADataExtractor()
        asteroid_data, approach_data = extractor.collect_data()
        
        # Insert data
        self.insert_data(asteroid_data, approach_data)
        
        self.close()
        print("Database setup completed!")

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.setup_database()