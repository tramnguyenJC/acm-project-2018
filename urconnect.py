from app import app, db
from app.models import User, Request

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Request': Request}

# start program with python3 urconnect.py to open in debug mode
if __name__ == "__main__":
	app.run(debug = True)
