# crear un entorno virtual con virtualenv
  escribir el comando para activarlo

  >> <nombre del entorno>\Scripts\activate.bat


  escribir para desactivarlo
    >> <nombre del entorno>\Scripts\desactivate.bat

## ingresar a la carpeta donde se encuentra el run.py
crear las variables de entorno

    ### Linux

    export FLASK_APP="run.py"
    export FLASK_ENV="development"

    #### Windows

    set "FLASK_APP=run.py"
    set "FLASK_ENV=development"

> Mi recomendación para las pruebas es que añadas esas variables en el fichero "activate" o "activate.bat"
> si estás usando virtualenv

## crear la tabla en la base de datos
tener el pgadmin4 (acuerdate de la contraseña que le colocas)

crear la base de datos con el nombre pdf
instalar flask-migrate
en la terminal, con el interprete de python ejecutar el siguiente codigo

>>flask db init<< solo se ejecuta una sola vez
(Después de ejecutarlo verás que se ha creado
dentro de la carpeta del proyecto un directorio llamado migrations. Este directorio debes añadirlo al sistema de control de versiones.)

>>flask db migrate -m "Initial database"
(Lo que hace este comando es generar un nuevo fichero con código python que incluye todos los cambios que hay seguir para actualizar la base de datos. Es un fichero de migración y se guarda en el directorio migrations/versions. Este directorio contiene todos los ficheros de migración de base de datos que se generan con Flask-Migrate. Dentro de él verás que tienes un fichero que se llama algo así como cb86527f8105_initial_database.py)

>>flask db upgrade (este es el ultimo paso para crear las tablas)

verificar si se crearon las tablas en la base de datos


## Ejecución con el servidor que trae Flask

Una vez que hayas descargado el proyecto, creado las variables de entorno y descargado las dependencias,
puedes arrancar el proyecto ejecutando:

    >>flask run

el flask run solo servira si se crearon las variables de entorno dichas anteriormente
