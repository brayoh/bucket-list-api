#!/usr/bin/env python
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app
from app.models import User, BucketList, Item

config = os.getenv("ENV")

app = create_app(config_name=config)

manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def createdb():
    db.create_all()
    print("database tables created successfully")


@manager.command
def dropdb():
    db.drop_all()
    print("database dropped")

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
