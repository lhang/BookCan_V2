from flask.ext.script import Manager,Server, Command
from flask.ext.migrate import MigrateCommand, Migrate
from server import app, db

manager = Manager(app)

app.debug = True
manager.add_command('run', Server())
manager.add_command('db', MigrateCommand)

@manager.command
def init_db():
    db.drop_all()
    db.create_all()
    print 'db init complete'

if __name__ == '__main__':
    manager.run()