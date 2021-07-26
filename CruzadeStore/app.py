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


carpeta = os.path.join('img')
app.config['carpeta'] = carpeta

#%% Uploads
@app.route('/img/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['carpeta'], nombreFoto)
#%%
#%% Home
@app.route('/')
def index():
    sql = "SELECT * FROM `cruzade`.`productos`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)    
        
    productos = cursor.fetchall()
    print('Información de la base de datos:\n',productos)    
    
    conn.commit()       
    #return render_template('productos.html', productos = productos) #Renderiza el index de productos 
    return render_template('index.html', productos = productos)
#%%

#%% Acerca de
@app.route('/Acerca_de')
def acerca():
    return render_template('Acerca_de.html')
#%%
#%% Contacto
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')
#%%
#%% Gestion
@app.route('/gestion/')
def gestion():
    sql = "SELECT * FROM `cruzade`.`productos`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)    
        
    productos = cursor.fetchall()
    print('Información de la base de datos:\n',productos)    
    
    conn.commit()       
    return render_template('gestion.html', productos = productos) 
#%%
#%% Create productos
@app.route('/productos/create')
def productCreate():
    return render_template('productos/create.html') #Renderiza create de productos
#%%

#%% Storage productos
@app.route('/productos/store',  methods=['POST'])

def storage():                             
    _nombre=request.form['txtNombre']  
    _precio=request.form['txtPrecio']  
    _foto=request.files['txtFoto']     
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename !='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("img/"+nuevoNombreFoto)
    
    sql="INSERT INTO `cruzade`.`productos` (`nomprod`,`precio`,`foto`) VALUES (%s,%s,%s)" 
    datos=(_nombre,_precio,nuevoNombreFoto) 

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)               
    conn.commit()
    return redirect('/gestion')  
#%%
#%% Edit productos
@app.route('/productos/edit/<int:id>')
def edit(id): 
    sql="SELECT * FROM `cruzade`.`productos` WHERE id=%s;" 
    conn=mysql.connect()              
    cursor=conn.cursor()              
    cursor.execute(sql,(id))          
    productos=cursor.fetchall() 
    conn.commit()
    print(productos) 
    return render_template('/productos/edit.html',productos=productos)
#%%

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
        _foto.save("img/"+nuevoNombreFoto)
   
        cursor.execute("SELECT foto FROM `cruzade`.`productos` WHERE id=%s",(id)) 

        fila=cursor.fetchall()   
        os.remove(os.path.join(app.config['carpeta'],fila[0][0]))
        cursor.execute("UPDATE productos SET foto=%s WHERE id=%s",(nuevoNombreFoto,id))
        conn.commit()

    cursor.execute(sql,datos)               
    conn.commit()
    return redirect('/gestion')
#%%

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
    return redirect('/gestion')
#%%

#%% Compra 
@app.route('/compra')
def compra():
    return render_template('compra.html')
#%%

#%% Login
@app.route('/login')
def loginpage():
    return render_template('login.html')
#%%

#%% Login ingreso
@app.route('/form_login', methods=['POST', 'GET'])
def login():
    name1 = request.form['username']
    pwd = request.form['password']

    sql = 'SELECT correo,password FROM `cruzade`.`empleados`;'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    database = cursor.fetchall()
    dictDatabase = dict(database)
    print(dictDatabase)

    conn.commit()
    if name1 not in dictDatabase:
        return render_template('login.html', info = 'Usuario invalido')
    else:
        if dictDatabase[name1] != pwd:
            return render_template('login.html', info = 'Contraseña invalida, si el problema persiste puede que no sea empleado, contactese con su superior')            
        else:
            return redirect('/gestion')
#%%
if __name__ == '__main__':
    app.run(debug = True)