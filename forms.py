from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    fullname = StringField('fullname', validators=[DataRequired(), Length(max=64)])
    username = StringField('username', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])

class uploadfileForm(FlaskForm):
    ourfile = FileField('Archivo', validators=[
        FileAllowed(['pdf', 'docx'] )])
    submit = SubmitField('Cargar')

class downloadForm(FlaskForm):
    submit = SubmitField('Descargar')

class searchForm(FlaskForm):
    consulta  = StringField('Buscar', validators=[DataRequired()])
    submit = SubmitField('buscar')

class ComentsForm(FlaskForm):
    title = StringField('Asunto', validators=[DataRequired(),Length(max=128)])
    post = TextAreaField('Post')
    submit = SubmitField('Comentar')
