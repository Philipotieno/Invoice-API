import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, models

from app.models import Database

app = create_app(config_name=os.getenv('APP_SETTINGS'))
db = Database()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def create_tables():
    db.create_tables()

@manager.command
def drop_tables():
    db.drop_tables()

if __name__ == '__main__':
    manager.run()
