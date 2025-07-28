#!/usr/bin/env python3
"""
Pantry CLI Application - Entry Point
A food management system supporting multiple countries and family recipes.
"""

import sys
import os
import traceback

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Add pantry subdirectory to path if it exists
pantry_dir = os.path.join(current_dir, 'pantry')
if os.path.exists(pantry_dir):
    sys.path.insert(0, pantry_dir)

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = {
        'mysql.connector': 'mysql-connector-python',
        'tabulate': 'tabulate',
        'dotenv': 'python-dotenv'
    }
    
    missing_packages = []
    for module, package in required_packages.items():
        try:
            __import__(module)                  
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Error: Missing required packages!")
        print("Please install the following packages:")
        for package in missing_packages:
            print(f"  pip install {package}")
        print("\nOr install all at once:")
        print(f"  pip install {' '.join(missing_packages)}")
        return False
    
    return True

def import_modules():
    """Import required modules with error handling"""
    try:
        # Try direct import first (files in same directory as main.py)
        from db import pantry_vault
        from cli import cli
        return pantry_vault, cli
    except ImportError as e1:
        try:
            # Try pantry subdirectory import
            from pantry.db import pantry_vault
            from pantry.cli import cli
            return pantry_vault, cli
        except ImportError as e2:
            print("Error: Cannot find required modules!")
            print(f"Direct import error: {e1}")
            print(f"Subdirectory import error: {e2}")
            print("\nPlease ensure the following files are in the same directory as main.py:")
            print("- config.py")
            print("- db.py")
            print("- crud.py")
            print("- cli.py")
            print(f"\nCurrent directory: {current_dir}")
            print(f"Files in current directory: {os.listdir(current_dir)}")
            if os.path.exists(pantry_dir):
                print(f"Files in pantry subdirectory: {os.listdir(pantry_dir)}")
            return None, None

def check_env_file():
    """Check if .env file exists and contains required variables"""
    env_path = os.path.join(current_dir, '.env')
    
    if not os.path.exists(env_path):
        print("Warning: .env file not found!")
        print("Please create a .env file with your database configuration:")
        print("DB_HOST=your_host")
        print("DB_PORT=your_port")
        print("DB_USER=your_username")
        print("DB_PASSWORD=your_password")
        print("DB_NAME=your_database_name")
        return False
    
    # Try to validate config
    try:
        from config import Config
        Config.validate_config()
        return True
    except Exception as e:
        print(f"Configuration error: {e}")
        print("Please check your .env file contains all required variables.")
        return False

def main():
    """Main entry point for the Pantry CLI application"""
    
    print("Starting Pantry CLI Application...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment configuration
    if not check_env_file():
        print("You can still run the application, but database connection may fail.")
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response not in ['y', 'yes']:
            sys.exit(1)
    
    # Import modules
    pantry_vault, cli = import_modules()
    if not pantry_vault or not cli:
        sys.exit(1)
    
    # Test database connection
    print("Testing database connection...")
    if not pantry_vault.connect():
        print("Failed to connect to database.")
        print("Please check your .env configuration and database credentials.")
        print("Make sure your MySQL server is running and accessible.")
        sys.exit(1)
    
    try:
        # Create tables if they don't exist
        print("Setting up database tables...")
        if not pantry_vault.create_tables():
            print("Failed to create database tables.")
            print("Please check your database permissions.")
            sys.exit(1)
        
        # Verify tables exist
        if not pantry_vault.check_tables_exist():
            print("Table verification failed.")
            sys.exit(1)
        
        print("Database setup completed successfully!")
        print("=" * 50)
        
        # Start the CLI application
        cli.run()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Full error traceback:")
        traceback.print_exc()
    finally:
        # Clean up database connection
        try:
            pantry_vault.disconnect()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        print("Application terminated successfully.")

if __name__ == "__main__":
    main()

