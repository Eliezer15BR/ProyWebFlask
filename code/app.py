from flask import Flask, render_template, request,redirect,url_for,jsonify
from flask_mysqldb import MySQL
app=Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyweb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


#######CATEGORIA################
@app.route('/categorias')
def categorias():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM categoria")
    datos=cursor.fetchall()
    cursor.close()
    return render_template('categorias.html',categorias=datos)

@app.route('/editar_categoria/<codigo_categoria>')
def editar_categoria(codigo_categoria):
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM categoria WHERE codigo_categoria= %s ",(codigo_categoria,))
    datos=cursor.fetchall()
    cursor.close()
    return render_template("formCategoria.html",categoria=datos[0])

@app.route('/actualiza_categoria/<codigo_categoria>',methods=['POST'])
def actualiza_categoria(codigo_categoria):
    if request.method== 'POST':
        nombre=request.form['nombre_categoria']
        cursor=mysql.connection.cursor()
        cursor.execute("UPDATE categoria SET nombre_categoria=%s WHERE codigo_categoria=%s",(nombre,codigo_categoria,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('categorias'))

@app.route('/nueva_categoria')
def nueva_categoria():
    return render_template("formCategoria.html")

@app.route('/agrega_categoria',methods=['POST'])
def agrega_categoria():
    if request.method=='POST':
        nombre_categoria=request.form['nombre_categoria']
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO categoria(nombre_categoria) VALUES(%s)",(nombre_categoria,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('categorias'))
    
@app.route('/eliminar_categoria/<codigo_categoria>')
def eliminar_categoria(codigo_categoria):
    cursor=mysql.connection.cursor()
    cursor.execute("DELETE FROM categoria WHERE codigo_categoria=%s",(codigo_categoria,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('categorias'))




############SUBCATEGORIAS####################

@app.route('/subcategorias')
@app.route('/subcategorias/<codigo_categoria>/<nombre_categoria>')
def subcategorias(codigo_categoria=None,nombre_categoria=None):
    cursor=mysql.connection.cursor()
    query="""
            SELECT * FROM categoria 
                JOIN subcategoria 
                ON categoria.codigo_categoria 
                LIKE subcategoria.codigo_categoria 
        """
    params=()
    if codigo_categoria:
        query+="WHERE subcategoria.codigo_categoria=%s"
        params=(codigo_categoria,)
    cursor.execute(query,params)
    datos=cursor.fetchall()
    cursor.close()
    return render_template('subcategorias.html',subcategorias=datos,nombre_categoria=nombre_categoria)

@app.route('/editar_subcategoria/<codigo_subcategoria>')
def editar_subcategoria(codigo_subcategoria):
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM subcategoria WHERE codigo_subcategoria= %s ",(codigo_subcategoria,))
    subcategoria=cursor.fetchall()
    cursor.execute("SELECT * FROM categoria")
    categorias=cursor.fetchall()
    cursor.close()
    return render_template("formSubcategoria.html",subcategoria=subcategoria[0],categorias=categorias)

@app.route('/actualiza_subcategoria/<codigo_subcategoria>',methods=['POST'])
def actualiza_subcategoria(codigo_subcategoria):
    if request.method== 'POST':
        nombre=request.form['nombre_subcategoria']
        codigo_categoria=request.form['codigo_categoria']
        cursor=mysql.connection.cursor()
        cursor.execute("UPDATE subcategoria SET nombre_subcategoria=%s,codigo_categoria=%s WHERE codigo_subcategoria=%s",(nombre,codigo_categoria,codigo_subcategoria,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('subcategorias'))

@app.route('/nueva_subcategoria')
def nueva_subcategoria():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM categoria")
    categorias=cursor.fetchall()
    cursor.close()
    return render_template("formSubcategoria.html",categorias=categorias)

@app.route('/agrega_subcategoria',methods=['POST'])
def agrega_subcategoria():
    if request.method=='POST':
        nombre_subcategoria=request.form['nombre_subcategoria']
        codigo_categoria=request.form['codigo_categoria']
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO subcategoria(nombre_subcategoria,codigo_categoria) VALUES(%s,%s)",(nombre_subcategoria,codigo_categoria,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('subcategorias'))
    
@app.route('/eliminar_subcategoria/<codigo_subcategoria>')
def eliminar_subcategoria(codigo_subcategoria):
    cursor=mysql.connection.cursor()
    cursor.execute("DELETE FROM subcategoria WHERE codigo_subcategoria=%s",(codigo_subcategoria,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('subcategorias'))    




##########ARTICULOS########################
@app.route('/articulos')
@app.route('/articulos/subcategoria/<codigo_subcategoria>/<nombre_subcategoria>/<nombre_categoria>',endpoint='articulos_por_subcategoria')
@app.route('/articulos/categoria/<codigo_categoria>/<nombre_categoria>',endpoint='articulos_por_categoria')
def articulos(codigo_subcategoria=None,nombre_subcategoria=None,codigo_categoria=None,nombre_categoria=None):
    cursor=mysql.connection.cursor()
    query="""
        SELECT * FROM articulo 
        JOIN subcategoria ON articulo.codigo_subcategoria = subcategoria.codigo_subcategoria 
        JOIN categoria ON articulo.codigo_categoria = categoria.codigo_categoria
    """
    params=()
    if codigo_subcategoria :
        query+="WHERE articulo.codigo_subcategoria=%s"
        params=(codigo_subcategoria,)
    if codigo_categoria:
        query+="WHERE articulo.codigo_categoria=%s"
        params=(codigo_categoria,)
    cursor.execute(query,params)
    datos=cursor.fetchall()
    cursor.close()
    return render_template('articulos.html',articulos=datos,nombre_categoria=nombre_categoria,nombre_subcategoria=nombre_subcategoria)

@app.route('/editar_articulo/<codigo_articulo>/<codigo_categoria>')
def editar_articulo(codigo_articulo,codigo_categoria):
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM articulo WHERE codigo_articulo= %s ",(codigo_articulo,))
    articulo=cursor.fetchall()
    cursor.execute("SELECT * FROM categoria")
    categorias=cursor.fetchall()
    cursor.execute("SELECT * FROM subcategoria WHERE codigo_categoria=%s",(codigo_categoria))
    subcategorias=cursor.fetchall()
    cursor.close()
    return render_template("formArticulo.html",articulo=articulo[0],categorias=categorias,subcategorias=subcategorias)

@app.route('/get_subcategorias/<codigo_categoria>')
def get_subcategorias(codigo_categoria):
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM subcategoria WHERE codigo_categoria=%s",(codigo_categoria,))
    subcategorias=cursor.fetchall()
    cursor.close()
    return jsonify(subcategorias)

@app.route('/actualiza_articulo/<codigo_articulo>',methods=['POST'])
def actualiza_articulo(codigo_articulo):
    if request.method=='POST':
        nombre_articulo=request.form['nombre_articulo']
        codigo_categoria=request.form['codigo_categoria']
        codigo_subcategoria=request.form['codigo_subcategoria']
        cursor=mysql.connection.cursor()
        cursor.execute("UPDATE articulo SET nombre_articulo=%s, codigo_categoria=%s, codigo_subcategoria=%s WHERE codigo_articulo=%s",(nombre_articulo,codigo_categoria,codigo_subcategoria,codigo_articulo,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('articulos'))

@app.route('/nuevo_articulo')
def nuevo_articulo():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM categoria")
    categorias=cursor.fetchall()
    cursor.close()
    return render_template("formArticulo.html",categorias=categorias)
    
@app.route('/agrega_articulo',methods=['POST'])
def agrega_articulo():
    if request.method=='POST':
        nombre_articulo=request.form['nombre_articulo']
        codigo_subcategoria=request.form['codigo_subcategoria']
        codigo_categoria=request.form['codigo_categoria']
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO articulo(nombre_articulo,codigo_categoria,codigo_subcategoria) VALUES(%s,%s,%s)",(nombre_articulo,codigo_categoria,codigo_subcategoria,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('articulos'))
    
@app.route('/elimina_articulo/<codigo_articulo>')
def elimina_articulo(codigo_articulo):
    cursor=mysql.connection.cursor()
    cursor.execute("DELETE FROM articulo WHERE codigo_articulo=%s",(codigo_articulo,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('articulos'))