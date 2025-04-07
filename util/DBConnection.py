
import mysql.connector
import os
from configparser import ConfigParser

class DBConnection:
    def __init__(self):
        self.config = ConfigParser()
        # Look for properties file in the project root
        self.property_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.properties')  # Default property file name

    def get_connection(self, property_file=None):
        """Reads database connection properties from a file and returns a connection"""
        if property_file:
            self.property_file = property_file

        try:
            if not os.path.exists(self.property_file):
                raise FileNotFoundError(f"Property file '{self.property_file}' not found")

            self.config.read(self.property_file)

            db_config = {
                'host': self.config.get('DEFAULT', 'host'),
                'database': self.config.get('DEFAULT', 'database'),
                'user': self.config.get('DEFAULT', 'user'),
                'password': self.config.get('DEFAULT', 'password'),
                'port': self.config.getint('DEFAULT', 'port'),
                'auth_plugin': 'mysql_native_password'  # Add this line
            }

            conn = mysql.connector.connect(**db_config)
            return conn

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        except mysql.connector.Error as e:
            print(f"Database Connection Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return None