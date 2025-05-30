import requests
import json
import sqlite3
from datetime import datetime, timedelta
import time
from config import NASA_API_KEY, BASE_URL, TARGET_RECORDS, DATABASE_NAME

class NASADataExtractor:
    def __init__(self):
        self.api_key = NASA_API_KEY
        self.base_url = BASE_URL
        self.asteroid_data = []
        self.approach_data = []
        
    def fetch_neo_data(self, start_date, end_date):
        """Fetch NEO data for given date range"""
        url = f"{self.base_url}?start_date={start_date}&end_date={end_date}&api_key={self.api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def extract_asteroid_fields(self, neo_data):
        """Extract required fields from NEO data"""
        for date, asteroids in neo_data['near_earth_objects'].items():
            for asteroid in asteroids:
                # Extract asteroid basic info
                asteroid_info = {
                    'id': int(asteroid['id']),
                    'name': asteroid['name'],
                    'absolute_magnitude_h': float(asteroid.get('absolute_magnitude_h', 0)),
                    'estimated_diameter_min_km': float(asteroid['estimated_diameter']['kilometers']['estimated_diameter_min']),
                    'estimated_diameter_max_km': float(asteroid['estimated_diameter']['kilometers']['estimated_diameter_max']),
                    'is_potentially_hazardous_asteroid': asteroid['is_potentially_hazardous_asteroid']
                }
                
                # Extract close approach data
                for approach in asteroid['close_approach_data']:
                    approach_info = {
                        'neo_reference_id': int(asteroid['id']),
                        'close_approach_date': approach['close_approach_date'],
                        'relative_velocity_kmph': float(approach['relative_velocity']['kilometers_per_hour']),
                        'astronomical': float(approach['miss_distance']['astronomical']),
                        'miss_distance_km': float(approach['miss_distance']['kilometers']),
                        'miss_distance_lunar': float(approach['miss_distance']['lunar']),
                        'orbiting_body': approach['orbiting_body']
                    }
                    
                    self.asteroid_data.append(asteroid_info)
                    self.approach_data.append(approach_info)
    
    def collect_data(self):
        """Main method to collect 10,000 records"""
        print("Starting data collection...")
        
        start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
        total_records = 0
        
        while total_records < TARGET_RECORDS:
            end_date = start_date + timedelta(days=6)  # 7-day range
            
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            print(f"Fetching data from {start_str} to {end_str}")
            
            neo_data = self.fetch_neo_data(start_str, end_str)
            
            if neo_data:
                self.extract_asteroid_fields(neo_data)
                total_records = len(self.asteroid_data)
                print(f"Total records collected: {total_records}")
                
                # Rate limiting - NASA API allows 1000 requests per hour
                time.sleep(1)
            else:
                print("Failed to fetch data. Retrying...")
                time.sleep(5)
            
            start_date = end_date + timedelta(days=1)
            
            # Safety check to avoid infinite loop
            if start_date.year > 2025:
                break
        
        # Trim to exactly TARGET_RECORDS
        self.asteroid_data = self.asteroid_data[:TARGET_RECORDS]
        self.approach_data = self.approach_data[:TARGET_RECORDS]
        
        print(f"Data collection completed. Total records: {len(self.asteroid_data)}")
        return self.asteroid_data, self.approach_data

if __name__ == "__main__":
    extractor = NASADataExtractor()
    asteroid_data, approach_data = extractor.collect_data()
    
    print(f"Collected {len(asteroid_data)} asteroid records")
    print(f"Collected {len(approach_data)} approach records")