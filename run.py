import os

from app import create_app

env_name = os.getenv('APP_SETTINGS')
app = create_app(env_name)

if __name__ == '__main__':
	app.run(debug=True) 