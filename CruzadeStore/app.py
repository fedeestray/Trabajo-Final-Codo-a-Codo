from flask import Flask
from flask import render_template, request, redirect, send_from_directory, url_for
from flaskext.mysql import MySQL
from datetime import datetime
import os
app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema' #CAMBIAR A NOMBRE DE BASE NUESTRA

mysql.init_app(app)


carpeta = os.path.join('uploads')
app.config['carpeta'] = carpeta

#%% Uploads
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['carpeta'], nombreFoto)
#%% Index
@app.route('/')
def index():
    sql = "SELECT * FROM `sistema`.`empleados`;" #CAMBIAR A CONSULTA RELACIONADA A NUESTRAS BASES Y TABLAS
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)    
        
    empleados = cursor.fetchall()
    print('Información de la base de datos:\n',empleados)    
    
    conn.commit()       
    return render_template('empleados/index.html', empleados = empleados)
#%% Create
@app.route('/create')
def create():
    return render_template('empleados/create.html')
#%% Storage
@app.route('/store',  methods=['POST'])     #CAMBIAR A CONSULTA RELACIONADA A NUESTRAS BASES Y TABLAS

# cuando formulario create.hmtl hace el submit envia los datos a /store
def  storage():                             
    _nombre=request.form['txtNombre']  # toma los datos txtNombre del form
    _correo=request.form['txtCorreo']  
    _foto=request.files['txtFoto']     
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename !='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    
    sql="INSERT INTO `sistema`.`empleados` (`nombre`,`correo`,`foto`) VALUES (%s,%s,%s)" #CAMBIAR A CONSULTA RELACIONADA A NUESTRAS BASES Y TABLAS
    #datos=(_nombre,_correo,_foto.filename)  # crea la sentencia sql
    datos=(_nombre,_correo,nuevoNombreFoto)  # crea la sentencia sql

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)               # ejecuta la sentencia sql 
    conn.commit()
    #return render_template('empleados/index.html')  # y renderiza index.html
    return redirect('/')  # y renderiza index.html
#%% Destroy
@app.route('/destroy/<int:id>')
def destroy(id):
    sql="DELETE  FROM `sistema`.`empleados` WHERE  id=%s;" #CAMBIAR A CONSULTA RELACIONADA A NUESTRAS BASES Y TABLAS
    
    conn=mysql.connect()              # me conecto a la base de datos
    cursor=conn.cursor()              # almacenar informacion 
    
    cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE id=%s",(id)) #CAMBIAR A CONSULTA RELACIONADA A NUESTRAS BASES Y TABLAS
    fila=cursor.fetchall()   # fila va a tener un solo registro y 1 solo campo
    os.remove(os.path.join(app.config['carpeta'],fila[0][0]))
        
    cursor.execute(sql,(id))               # ejecuto en MySQL la variable sql
    conn.commit()
    return redirect('/')                 # reidrecciona al '/'

#%% Edit
@app.route('/edit/<int:id>')
def edit(id): 
    sql="SELECT * FROM `sistema`.`empleados` WHERE id=%s;" #CAMBIAR A CONSULTA RELACIONADA A NUESTRAS BASES Y TABLAS
    conn=mysql.connect()              # me conecto a la base de datos
    cursor=conn.cursor()              # almacenar informacion 
    cursor.execute(sql,(id))               # ejecuto en MySQL la variable sql
    empleados=cursor.fetchall() #CAMBIAR A NUESTRA TABLA
    conn.commit()
    print(empleados) #CAMBIAR A NUESTRA TABLA
    return render_template('empleados/edit.html',empleados=empleados) #CAMBIAR A DATOS NUESTRA TABLA
#%% Update
@app.route('/update',  methods=['POST']) #CAMBIAR A DATOS DE NUESTRA TABLA

# cuando formulario create.hmtl hace el submit envia los datos a /store
def  update():                             
    _nombre=request.form['txtNombre']  # toma los datos txtNombre del form
    _correo=request.form['txtCorreo']  
    _foto=request.files['txtFoto']     
    id=request.form['txtId']

    sql="UPDATE `sistema`.`empleados` SET  `nombre`=%s  ,`correo`=%s WHERE id=%s" #CAMBIAR A CONSULTA RELACIONADA A NUESTRAS BASES Y TABLAS
    datos=(_nombre,_correo,id)  # crea la sentencia sql
    conn=mysql.connect()
    cursor=conn.cursor()

# agregamos
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename !='':  # igual que en /store
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
   
        cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE id=%s",(id)) #CAMBIAR A CONSULTA RELACIONADA A NUESTRAS BASES Y TABLAS

        fila=cursor.fetchall()   # fila va a tener un solo registro y 1 solo campo
        os.remove(os.path.join(app.config['carpeta'],fila[0][0]))
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s",(nuevoNombreFoto,id)) #CAMBIAR A CONSULTA RELACIONADA A NUESTRAS BASES Y TABLAS
        conn.commit()

    cursor.execute(sql,datos)               # ejecuta la sentencia sql 
    conn.commit()
    return redirect('/')  # y renderiza index.html

#%%

if __name__ == '__main__':
    app.run(debug = True)