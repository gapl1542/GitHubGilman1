from flask import url_for
from flask_login import UserMixin
#from sqlalchemy.exc import IntergrityError
from werkzeug.security import generate_password_hash, check_password_hash
from run import db
import datetime
from flask_whooshee import Whooshee, AbstractWhoosheer
from run import whooshee





class User(db.Model, UserMixin):

    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80),unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_teacher = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    fav_account = db.relationship('Favoritos', backref='account')
    Our_files_user = db.relationship('Our_Files', backref='account')
    coments_user = db.relationship('Coments_pdf', backref='account')

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

class Favoritos(db.Model):
    __tablename__ ='favorites'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('account.id'))
    id_pdf = db.Column(db.Integer)


class Coments_pdf(db.Model):

    __tablename__ = 'coments'
    id = db.Column(db.Integer, primary_key=True)
    #id_user_pdf = db.Column(db.Integer, db.PrimarykeyContrain('account.id','files.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('account.id'))
    username = db.Column(db.String(80), nullable=False)
    username_pdf= db.Column(db.String(80), nullable=False)
    id_pdf=db.Column(db.Integer)
    title_coments = db.Column(db.String(256), nullable=False)
    uptime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title_pdf =db.Column(db.String(256), nullable=False,unique=True)
    post = db.Column(db.Text, nullable=False)

    @staticmethod
    def get_by_username(username):
        return Coments_pdf.query.filter_by(username=username).first()



@whooshee.register_model('username','texto_completo')
class Our_Files(db.Model):

    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    routes_files = db.Column(db.String(256), nullable=False)
    title = db.Column(db.String(256), nullable=False,unique=True)
    uptime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    category = db.Column(db.String(256), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('account.id'))
    texto_completo = db.Column(db.Text, nullable=False)

    def get_by_id_user(id_user):
        return Our_files.query.get(id_user)

    @staticmethod
    def get_by_username(username):
        return Our_Files.query.filter_by(username=username).first()

    @staticmethod
    def get_by_title(title):
        return Our_Files.query.filter_by(title=title).first()
