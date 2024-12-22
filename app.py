from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Cambia esto según tu configuración
app.config['MYSQL_PASSWORD'] = ''  # Cambia esto según tu configuración
app.config['MYSQL_DB'] = 'peliculas_db'

mysql = MySQL(app)

# Ruta para mostrar todas las películas
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM peliculas")
    peliculas = cursor.fetchall()
    cursor.close()
    return render_template('index.html', peliculas=peliculas)

# Ruta para crear una nueva película
@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        titulo = request.form['titulo']
        director = request.form['director']
        genero = request.form['genero']
        anio = request.form['anio']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO peliculas (titulo, director, genero, anio) VALUES (%s, %s, %s, %s)",
                       (titulo, director, genero, anio))
        mysql.connection.commit()
        cursor.close()
        flash('Película agregada exitosamente.')
        return redirect('/')
    
    return render_template('crear.html')

# Ruta para editar una película
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM peliculas WHERE id = %s", (id,))
    pelicula = cursor.fetchone()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        director = request.form['director']
        genero = request.form['genero']
        anio = request.form['anio']
        
        cursor.execute("UPDATE peliculas SET titulo = %s, director = %s, genero = %s, anio = %s WHERE id = %s",
                       (titulo, director, genero, anio, id))
        mysql.connection.commit()
        flash('Película actualizada exitosamente.')
        return redirect('/')
    
    cursor.close()
    return render_template('editar.html', pelicula=pelicula)

# Ruta para eliminar una película
@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM peliculas WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash('Película eliminada exitosamente.')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
