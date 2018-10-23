from rt.rt import db
from datetime import datetime


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    url = db.Column(db.String(100))
    summary = db.Column(db.String(200))
    count = db.Column(db.Integer, default=0)
    last_update = db.Column(db.DateTime, default=datetime.now())
    pages = db.relationship('Page', backref='article', lazy='dynamic')

    def __repr__(self):
        return '<%s>'%self.title


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    title = db.Column(db.String(50))
    url = db.Column(db.String(100))
    content = db.Column(db.Text)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)

