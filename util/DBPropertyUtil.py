import configparser
import os

def get_db_properties():
    config = configparser.ConfigParser()
    properties_file = os.path.join(os.path.dirname(__file__), "db.properties")

    if not os.path.exists(properties_file):
        raise FileNotFoundError(f"The DB {properties_file} file isn't there")

    config.read(properties_file)

    try:
        return {
            "host": config.get("DEFAULT", "db.host"),
            "port": config.get("DEFAULT", "db.port"),
            "user": config.get("DEFAULT", "db.user"),
            "password": config.get("DEFAULT", "db.password"),
            "database": config.get("DEFAULT", "db.name"),}
    except Exception as e:
        raise Exception(f"Error reading database properties: {e}")