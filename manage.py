from flask.ext.script import Manager,Server
from flask.ext.migrate import MigrateCommand, Migrate
from server import app, db

manager = Manager(app)

app.debug = True
manager.add_command('run', Server())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()