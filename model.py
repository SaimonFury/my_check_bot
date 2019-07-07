from  flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, unique=True)
    role = db.Column(db.String(10), index=True)

    def __repr__(self):
        return f'<Student: {self.username}>'