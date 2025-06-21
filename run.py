import sys
print("run.py script started", file=sys.stderr) # Immediate print

import os
from hermitta_app import create_app

try:
    print("Attempting to call create_app()", file=sys.stderr)
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    print("create_app() returned successfully", file=sys.stderr)

    if __name__ == '__main__':
        host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
        port = int(os.getenv('FLASK_RUN_PORT', os.getenv('PORT', 5000)))

        print(f"Attempting to start Flask app with app.run() on {host}:{port}", file=sys.stderr)
        app.run(host=host, port=port)
        print("app.run() finished or was interrupted", file=sys.stderr) # Should not be reached if server runs until killed

except Exception as e:
    print(f"Error during Flask app startup in run.py: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
