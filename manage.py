from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from start import app,db
from models import first_crawl
from flask_sqlalchemy import SQLAlchemy
import config

manager = Manager(app)

#使用migrate绑定app和db
migrate = Migrate(app, db)

#添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)



class first_crawl(db.Model):
    __tablename__ = 'first_crawl'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(255), nullable=False)
    NewsURL = db.Column(db.String(255), nullable=False)
    src = db.Column(db.String(40), nullable=False)
    time = db.Column(db.String(20), nullable=False)


class second_crawl(db.Model):
    __tablename__ = "second_crawl"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    NewsURL = db.Column(db.String(255), nullable=False)
    visit_time = db.Column(db.Integer, nullable=False)
    src = db.Column(db.String(64), nullable=False)
    time = db.Column(db.String(20), nullable=False)


if __name__ == "__main__":
    manager.run()