
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse

from flask import Flask, render_template, send_file



from forms import SignupForm, PostForm, LoginForm, uploadfileForm, downloadForm, ComentsForm




from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy

import PyPDF2

import os
from os import path
from os import remove
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed

from os.path import abspath, dirname, join

from flask_migrate import Migrate

from datetime import timedelta

import fitz

import carga_modelo as cm

import mediaf as mf
import contador_palabras as cp

from flask_whooshee import Whooshee, AbstractWhoosheer

# Define the application directory
#BASE_DIR = dirname(dirname(abspath(__file__)))
# Media dir
#MEDIA_DIR = join(BASE_DIR, 'archivos')
#POSTS_IMAGES_DIR = join(MEDIA_DIR, 'pdfs')


app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5022fran@localhost:5432/pdf'
app.config['UPLOAD_FOLDER'] = './Archivos'
login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)
whooshee = Whooshee()
migrate = Migrate()
db.init_app(app)
whooshee.init_app(app)
migrate.init_app(app, db)
from models import User, Our_Files, Coments_pdf, Favoritos
csrf = CSRFProtect(app)

@app.route("/mfire")
def mediaFIRE():
    response = mf.media()
    print(response['user_info']['display_name'])
    return redirect(url_for('home'))


@app.route("/result", methods=['GET'])
def result():

    cadenas = request.args.get('texto')
    #print(type(text))
    #cadenas = str(text)
    #print(cadenas)
    if current_user.is_authenticated:
        fil = (Our_Files.query.\
            whooshee_search(cadenas).\
            order_by(Our_Files.texto_completo.desc()).\
            all())
        return render_template("results.html", fil = fil )
    return redirect(url_for('home'))



@app.route("/show_coments")
def show_coments():
    if current_user.is_authenticated:
        coment=db.session.query(Coments_pdf).all()  #en fil se guardan todos los archivos subidos del usuario actual
        for comenta in coment:
            print(comenta.title_pdf)
            print(comenta.uptime)
        #fil = files.query.filter_by(id_user=id_user).first()
        return render_template("comentarios.html", coment = coment )
    return redirect(url_for('home'))



@app.route('/download/<filetitle>', methods=['GET'])
def return_file(filetitle):
    if current_user.is_authenticated:
        #filetitle = file.title
    # Descargar archivos subidos al directorio UPLOAD_FOLDER
        try:
            return send_file(app.config['UPLOAD_FOLDER']+"/"+str(filetitle))
        except Exception as e:
            return str(e)
    return redirect(url_for('home'))





@app.route("/show_file/<filetitle>/<username>")
def show_files(filetitle, username):
    if current_user.is_authenticated:
        acc = User.get_by_username(username)
        file = Our_Files.get_by_title(filetitle)
        #id_user = current_user.id
        #acc = db.session.query(User).get(id_user)
        #fil=db.session.query(Our_Files).filter_by(id_user=id_user).all()  #en fil se guardan todos los archivos subidos del usuario actual
        #fil = files.query.filter_by(id_user=id_user).first()
        form = ComentsForm()
        return render_template("visualizar_archivo.html", file = file, acc = acc ,form = form)
    return redirect(url_for('home'))

@app.route("/coments/<username_pdf>/<id_pdf>/<title_pdf>",methods=['GET', 'POST'])
def comentspostForm(username_pdf, id_pdf,title_pdf):
    if current_user.is_authenticated:
        form = ComentsForm()

        # obtenemos el archivo del input "archivo"

        if form.validate_on_submit():

            title = form.title.data
            post = form.post.data
            id_user = current_user.id
            username = current_user.username
            ### guardar en la base de datos
            comen = Coments_pdf(id_user = id_user, username = username, username_pdf = username_pdf, id_pdf = id_pdf,title_coments = title, post=post, title_pdf = title_pdf)
            db.session.add(comen)
            db.session.commit()

        return redirect(url_for('home'))




@app.route("/show_pdf")
def show_pdf():
    if current_user.is_authenticated:
        id_user = current_user.id
        acc = db.session.query(User).get(id_user)
        fil=db.session.query(Our_Files).filter_by(id_user=id_user).all()  #en fil se guardan todos los archivos subidos del usuario actual
        #fil = files.query.filter_by(id_user=id_user).first()
        return render_template("mis_archivos.html", fil = fil, acc =acc )
    return redirect(url_for('home'))


@app.route("/up")
def cargar():
    if current_user.is_authenticated:
        form = uploadfileForm()
        return render_template("cargar.html", form=form)
    return redirect(url_for('home'))

## carga de archivos
@app.route("/upload", methods=['GET', 'POST'])
def uploader():
    if current_user.is_authenticated:
        form = uploadfileForm()
        error = None

        # obtenemos el archivo del input "archivo"
        if form.validate_on_submit():
            ourfile = form.ourfile.data
            title= secure_filename(ourfile.filename)
            id_user = current_user.id
            username = current_user.username

            use_pdf = Our_Files.get_by_title(title)
            if use_pdf is not None:
                   error = f'Cambie el nombre del archivo. {title} ya está siendo utilizado'
            else:
                # Guardamos el archivo en el directorio "Archivos PDF"
                ourfile.save(os.path.join(app.config['UPLOAD_FOLDER'], title))
                ruta_relativa = 'Archivos/' + title
                routes_files = path.abspath(ruta_relativa)
                #ourfile.save(os.path.join(app.path, title))
                #convertir y guardar el pdf a text
                doc = fitz.open(os.path.join(app.config['UPLOAD_FOLDER'], title))
                #print("numero de paginas: ", doc.pageCount)
                #print("metadatos: ", doc.metadata)
                salida = open('./prueba/archivoTXT.txt',"wb")
                pagina = doc.loadPage(0)
                texto_completo = "inicio"
                separador = "------"
                for pagina in doc:
                    texto = pagina.getText().encode("utf8")
                    salida.write(texto)
                    texto_completo = texto_completo + str(texto)
                    texto_completo = texto_completo + separador
                    salida.write(b"\n------\n")
                salida.close()
                salida = open('./prueba/archivoTXT.txt',"r",encoding="utf8")
                y = cp.keywords(salida)
                salida.close()
                with open('./palabras_clave/'+title+'.txt',"w",encoding="utf8") as t: #
                    for k,v in y.items():
                        t.write(f'{k} {v}\n')
                    #print(y)
            ####Clasificador######
                category = cm.clasificador()
            ######## cierre clasificador#####
                remove('./prueba/archivoTXT.txt') ## quita el archivo temporal
            #
            ### guardar en la base de datos
                ourfiles = Our_Files(routes_files = routes_files, title=title, id_user = id_user, category = category, username = username, texto_completo = texto_completo)
                db.session.add(ourfiles)
                db.session.commit()
                return redirect(url_for('home'))
            return render_template('cargar.html', form = form, error = error)
        return redirect(url_for('home'))
    return redirect(url_for('home'))
## fin carga de archivos


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        fullname = form.fullname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
               error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            user = User.get_by_username(username)
            if user is not None:
                   error = f'El username {username} ya está siendo utilizado por otro usuario'
            else:
                # Creamos el usuario y lo guardamos
                user = User(fullname=fullname,username=username, email=email)
                user.set_password(password)
                user.save()
                # Dejamos al usuario logueado
                login_user(user, remember=True)
                next_page = request.args.get('next', None)
                if not next_page or url_parse(next_page).netloc != '':
                    print (password)
                    next_page = url_for('index') #aqui deberia ir al home page del ussuario
                    return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)


## tiempo para caducidad de session
@app.before_request
def before_request():
    #.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
##

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route('/home')
def home():
    if current_user.is_authenticated:
        id = current_user.id
        acc = db.session.query(User).get(id)
        fil=db.session.query(Our_Files).all()  #en fil se guardan todos los archivos subidos del usuario actual



        return render_template("home.html", fil = fil, acc =acc )
    return redirect(url_for('login'))

@app.route('/')
def profile():
    # Check if user is loggedin
    if current_user.is_authenticated:
        # We need all the account info for the user so we can display it on the profile page
        id = current_user.id
        acc = db.session.query(User).get(id)

        # Show the profile page with account info
        return render_template('profile.html', account=acc)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))





@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))





@app.route("/index")
def index():

    band = False
    if current_user.is_authenticated:
        band = True
        username = current_user.username
        return render_template("index.html", band=band, username=username)
    return render_template("index.html", band=band)




if __name__ == '__main__':
    app.run(debug=True)
