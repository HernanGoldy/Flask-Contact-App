from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app= Flask(__name__)

# Conección a MySQL
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'flaskcontacts'
mysql= MySQL(app)

# Inicializamos una sesión para guardar los datos y luego reutilizarlos
app.secret_key= 'mysecretkey' #NOTA -> secret_key indica la forma en que protegemos la sesión


@app.route('/')
def index():
    # Hacemos la consulta a la BD y la guardamos en una variable
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    # Ejecutamos la consulta y la guardamos en una variable
    data= cur.fetchall()
    return render_template('index.html', contacts=data)

@app.route('/add_contact', methods= ['POST'])
def add_contac():
    if request.method == 'POST':
        fullname= request.form['fullname']
        phone= request.form['phone']
        email= request.form['email']
        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()
        #NOTA -> flash nos permite enviar un mensaje luego de insertar un dato
        flash('Contact Added Successfully')
        return redirect(url_for('index'))

@app.route('/edit')
def edit_contact():
    return "edit contact"

@app.route('/delete/<string:id>')
def delete_contact(id):
    # Pasamos la consulta a mysql para que elimine el id y lo guardamos en una variable
    cur= mysql.connection.cursor()
    # Hacemos la consulta a mysql
    cur.execute('DELETE FROM contacts WHERE id={0}'.format(id)) #NOTA -> Otra forma de consultar
    mysql.connection.commit()
    # Antes de redireccionar pasamos una msj.
    flash('Contact Removed Successfully')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
