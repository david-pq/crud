from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_db():
    with sqlite3.connect('almacen.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS producto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        conn.commit()

init_db()


@app.route('/')
def index():
    with sqlite3.connect('almacen.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM producto")
        productos = cursor.fetchall()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        with sqlite3.connect('almacen.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)",
                           (descripcion, cantidad, precio))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    with sqlite3.connect('almacen.db') as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            cantidad = int(request.form['cantidad'])
            precio = float(request.form['precio'])
            cursor.execute("UPDATE producto SET descripcion=?, cantidad=?, precio=? WHERE id=?",
                           (descripcion, cantidad, precio, id))
            conn.commit()
            return redirect(url_for('index'))
        cursor.execute("SELECT * FROM producto WHERE id=?", (id,))
        producto = cursor.fetchone()
    return render_template('editar.html', producto=producto)


@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar(id):
    with sqlite3.connect('almacen.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM producto WHERE id=?", (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
