from app import app, db
from app.models import User, Post, Request

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post, 'Request': Request}

# start program with python3 urconnect.py to open in debug mode
if __name__ == "__main__":
	app.run(debug = True)
