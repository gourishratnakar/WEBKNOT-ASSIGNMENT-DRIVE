import subprocess
import sys
import time
import threading
from init_db import init_sample_data

def run_flask_app():
    """Run the Flask application in a separate thread"""
    subprocess.run([sys.executable, 'app.py'])

def main():
    print("🚀 Campus Event Management Platform - Demo")
    print("=" * 60)

    # Initialize database with sample data
    print("1. Initializing database with sample data...")
    init_sample_data()

    print("\n2. Starting Flask server...")
    print("   Server will start at: http://127.0.0.1:5000")
    print("   API endpoints available at: http://127.0.0.1:5000/api")

    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()

    # Wait for server to start
    time.sleep(3)

    print("\n3. Running API tests to demonstrate functionality...")
    print("   This will test all endpoints and show outputs")

    # Run the test script
    try:
        subprocess.run([sys.executable, 'test_api.py'])
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError running tests: {e}")
        print("Make sure the server is running and try running 'python test_api.py' manually")

    print("\n✅ Demo completed!")
    print("\n📋 Next Steps:")
    print("1. Flask server is running at http://127.0.0.1:5000")
    print("2. Test the API endpoints using the test script: python test_api.py")
    print("3. Or use tools like Postman/curl to test individual endpoints")
    print("4. Check the database file: campus_events.db")

if __name__ == '__main__':
    main()