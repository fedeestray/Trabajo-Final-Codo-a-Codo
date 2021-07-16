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
app.config['MYSQL_DATABASE_DB'] = 'cruzade' 

mysql.init_app(app)


carpeta = os.path.join('uploads')
app.config['carpeta'] = carpeta

#%% Uploads
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['carpeta'], nombreFoto)
#%% Index empleados
@app.route('/')
def index():
    sql = "SELECT * FROM `cruzade`.`empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)    
        
    empleados = cursor.fetchall()
    print('Información de la base de datos:\n',empleados)    
    
    conn.commit()       
    return render_template('empleados/index.html', empleados = empleados)
#%% Create empleados
@app.route('/create')
def create():
    return render_template('empleados/create.html')
#%% Storage empleados
@app.route('/store',  methods=['POST'])     
# cuando formulario create.hmtl hace el submit envia los datos a /store

def storage():                             
    _nombre=request.form['txtNombre'] 
    _correo=request.form['txtCorreo']  
    _foto=request.files['txtFoto']     
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename !='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    
    sql="INSERT INTO `cruzade`.`empleados` (`nomap`,`correo`,`foto`) VALUES (%s,%s,%s)" #Creo la sentencia sql
    datos=(_nombre,_correo,nuevoNombreFoto)

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)               # ejecuta la sentencia sql 
    conn.commit()
    
    return redirect('/')  # y renderiza index.html
#%% Destroy empleados
@app.route('/destroy/<int:id>')
def destroy(id):
    sql="DELETE  FROM `cruzade`.`empleados` WHERE  id=%s;"     
    conn=mysql.connect()              # me conecto a la base de datos
    cursor=conn.cursor()              # almacena informacion 
    
    cursor.execute("SELECT foto FROM `cruzade`.`empleados` WHERE id=%s",(id)) 

    fila=cursor.fetchall()   # fila va a tener un solo registro y 1 solo campo
    os.remove(os.path.join(app.config['carpeta'],fila[0][0]))
        
    cursor.execute(sql,(id))               # ejecuto en MySQL la variable sql
    conn.commit()
    return redirect('/')                 # redirecciona al 'index de empleados'

#%% Edit empleados
@app.route('/edit/<int:id>')
def edit(id): 
    sql="SELECT * FROM `cruzade`.`empleados` WHERE id=%s;" 
    conn=mysql.connect()              
    cursor=conn.cursor()               
    cursor.execute(sql,(id))          
    empleados=cursor.fetchall() 
    conn.commit()
    print(empleados) 
    return render_template('empleados/edit.html',empleados=empleados) 
#%% Update empleados
@app.route('/update',  methods=['POST']) 

# cuando formulario create.hmtl hace el submit envia los datos a /store
def  update():                             
    _nombre=request.form['txtNombre']  
    _correo=request.form['txtCorreo']  
    _foto=request.files['txtFoto']     
    id=request.form['txtId']

    sql="UPDATE `cruzade`.`empleados` SET  `nomap`=%s  ,`correo`=%s WHERE id=%s" 
    datos=(_nombre,_correo,id)  
    conn=mysql.connect()
    cursor=conn.cursor()

# agregamos
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename !='':  
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
   
        cursor.execute("SELECT foto FROM `cruzade`.`empleados` WHERE id=%s",(id)) 

        fila=cursor.fetchall()   
        os.remove(os.path.join(app.config['carpeta'],fila[0][0]))
        cursor.execute("UPDATE `cruzade`.`empleados` SET foto=%s WHERE id=%s",(nuevoNombreFoto,id)) 
        conn.commit()

    cursor.execute(sql,datos)               
    conn.commit()
    return redirect('/')  # y renderiza index.html de empleados

#%% Index productos
@app.route("/productos/")
def productIndex():
    sql = "SELECT * FROM `cruzade`.`productos`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)    
        
    productos = cursor.fetchall()
    print('Información de la base de datos:\n',productos)    
    
    conn.commit()       
    return render_template('productos/index.html', productos = productos) #Renderiza el index de productos
#%% Create productos
@app.route('/productos/create')
def productCreate():
    return render_template('productos/create.html') #Renderiza create de productos
#%% Storage productos
@app.route('/productos/store',  methods=['POST'])
# cuando formulario create.hmtl hace el submit envia los datos a /store de productos
def productStorage():                             
    _nombre=request.form['txtNombre']  
    _precio=request.form['txtPrecio']  
    _foto=request.files['txtFoto']     
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename !='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    
    sql="INSERT INTO `cruzade`.`productos` (`nomprod`,`precio`,`foto`) VALUES (%s,%s,%s)" 
    datos=(_nombre,_precio,nuevoNombreFoto) 

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)               
    conn.commit()
    return redirect('/productos/')  # y renderiza index.html de productos
#%% Edit productos
@app.route('/productos/edit/<int:id>')
def productEdit(id): 
    sql="SELECT * FROM `cruzade`.`productos` WHERE id=%s;" 
    conn=mysql.connect()              
    cursor=conn.cursor()              
    cursor.execute(sql,(id))          
    productos=cursor.fetchall() 
    conn.commit()
    print(productos) 
    return render_template('productos/edit.html',productos=productos) 
#%% Update productos
@app.route('/productos/update',  methods=['POST']) 

# cuando formulario create.hmtl hace el submit envia los datos a /store de productos
def productosUpdate():                             
    _nombre=request.form['txtNombre'] 
    _precio=request.form['txtPrecio']  
    _foto=request.files['txtFoto']     
    id=request.form['txtId']

    sql="UPDATE `cruzade`.`productos` SET  `nomprod`=%s  ,`precio`=%s WHERE id=%s" 
    datos=(_nombre,_precio,id)  
    conn=mysql.connect()
    cursor=conn.cursor()

# agregamos
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename !='':  
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
   
        cursor.execute("SELECT foto FROM `cruzade`.`productos` WHERE id=%s",(id)) 

        fila=cursor.fetchall()   
        os.remove(os.path.join(app.config['carpeta'],fila[0][0]))
        cursor.execute("UPDATE productos SET foto=%s WHERE id=%s",(nuevoNombreFoto,id))
        conn.commit()

    cursor.execute(sql,datos)               
    conn.commit()
    return redirect('/productos/')  #Renderiza index.html de productos

#%% Destroy productos
@app.route('/productos/destroy/<int:id>')
def productDdestroy(id):
    sql="DELETE  FROM `cruzade`.`productos` WHERE  id=%s;" 
    
    conn=mysql.connect()              
    cursor=conn.cursor()                  
    cursor.execute("SELECT foto FROM `cruzade`.`productos` WHERE id=%s",(id)) 
    fila=cursor.fetchall()   
    os.remove(os.path.join(app.config['carpeta'],fila[0][0]))
        
    cursor.execute(sql,(id)) 
    conn.commit()
    return redirect('/productos/')                 # reidrecciona al '/' de productos

#%%
if __name__ == '__main__':
    app.run(debug = True)