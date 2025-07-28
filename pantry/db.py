import mysql.connector
from config import Config
from mysql.connector import Error as MySQLError

def get_connection():
    """
    Returns a live MySQL connection.

    Raises
    ------
    ConnectionError
        If the underlying connector cannot establish a connection.
    """
    try:
        return mysql.connector.connect(**Config)
    except mysql.connector.Error as exc: 
        # Optionally add structured logging here
        raise ConnectionError("Could not establish MySQL connection") from exc

class PantryVault:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.current_user = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**Config.get_connection_params())
            self.cursor = self.conn.cursor(dictionary=True)
            return True
        except mysql.connector.Error as exc:
            print(f"Database connection error: {exc}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.cursor = None
        self.conn = None

    def ensure_connection(self):
        if not self.conn or not self.cursor:
            self.connect()

    def create_tables(self):
        self.ensure_connection()
        # Placeholder: Implement actual table creation logic
        try:
            # Example: create a countries table if not exists
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS countries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE
                )
            ''')
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating tables: {e}")
            return False

    def check_tables_exist(self):
        self.ensure_connection()
        # Placeholder: Check if required tables exist
        try:
            self.cursor.execute("SHOW TABLES LIKE 'countries'")
            result = self.cursor.fetchone()
            return bool(result)
        except Exception as e:
            print(f"Error checking tables: {e}")
            return False

    def execute_query(self, query, params=None):
        self.ensure_connection()
        try:
            self.cursor.execute(query, params or ())
            return [dict(row) for row in self.cursor.fetchall()]
        except MySQLError as e:
            if getattr(e, 'errno', None) == 2055 or 'SSL' in str(e) or 'connection was forcibly closed' in str(e):
                print("Lost connection to MySQL server. Attempting to reconnect...")
                self.connect()
                try:
                    self.cursor.execute(query, params or ())
                    return [dict(row) for row in self.cursor.fetchall()]
                except Exception as e2:
                    print(f"Query error after reconnect: {e2}")
                    return []
            print(f"Query error: {e}")
            return []
        except Exception as e:
            print(f"Query error: {e}")
            return []

    def execute_update(self, query, params=None):
        self.ensure_connection()
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return self.cursor.rowcount
        except MySQLError as e:
            if getattr(e, 'errno', None) == 2055 or 'SSL' in str(e) or 'connection was forcibly closed' in str(e):
                print("Lost connection to MySQL server. Attempting to reconnect...")
                self.connect()
                try:
                    self.cursor.execute(query, params or ())
                    self.conn.commit()
                    return self.cursor.rowcount
                except Exception as e2:
                    print(f"Update error after reconnect: {e2}")
                    return 0
            print(f"Update error: {e}")
            return 0
        except Exception as e:
            print(f"Update error: {e}")
            return 0

    def validate_user(self, username, password):
        self.ensure_connection()
        # Placeholder: Implement actual user validation
        # Example: check if user exists in users table
        try:
            self.cursor.execute("SELECT * FROM users WHERE user_name=%s AND password=%s", (username, password))
            user = self.cursor.fetchone()
            if user:
                self.current_user = user
                return True
            return False
        except Exception as e:
            print(f"User validation error: {e}")
            return False

    def register_user(self, username, email, password, country_id=None):
        self.ensure_connection()
        try:
            self.cursor.execute(
                "INSERT INTO users (user_name, email, password, country_id) VALUES (%s, %s, %s, %s)",
                (username, email, password, country_id)
            )
            self.conn.commit()
            return True, "Registration successful."
        except Exception as e:
            print(f"User registration error: {e}")
            return False, f"Registration failed: {e}"

    def get_current_user(self):
        return self.current_user

    def logout(self):
        self.current_user = None

# Instantiate pantry_vault for import
pantry_vault = PantryVault()