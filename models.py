from exts import db

class first_crawl(db.Model):
    __tablename__ = 'first_crawl'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(60), nullable=False)
    NewsURL = db.Column(db.String(255), nullable=False)
    src = db.Column(db.String(20), nullable=False)
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