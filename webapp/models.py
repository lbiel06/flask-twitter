from webapp import db
import textwrap

# Models

class User(db.Model):
    query: db.Query
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    is_admin = db.Column(db.Boolean)
    tweets = db.relationship('Tweet', backref='User')

    def __init__(self, username, password, is_admin=False) -> None:
        self.username = username
        self.password = password
        self.is_admin = is_admin
    
    def __repr__(self) -> str:
        return textwrap.dedent(f'''
        User
            username: {self.username},
            password: {self.password},
            admin: {self.is_admin}
        ''')


class Tweet(db.Model):
    query: db.Query
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    text = db.Column(db.String)
    date = db.Column(db.DateTime)

    def __init__(self, username, text, date) -> None:
        self.username = username
        self.text = text
        self.date = date

    def __repr__(self) -> str:
        return textwrap.dedent(f'''
        Tweet
            id: {self.tid}
            user: {self.username}
            text: {self.text}
            date: {self.date}
            ''')
