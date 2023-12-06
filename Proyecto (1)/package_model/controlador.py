from package_model.bd import BD
#localidades
def listarLocalidades():
    bd = BD()
    bd.connect()
    consulta = "SELECT l.Localidad, COUNT(c.id) as habitantes FROM localidad l LEFT JOIN viviendas v ON l.Localidad = v.locacion LEFT JOIN clientes c ON v.nombre = c.direccion GROUP BY l.Localidad"
    try:
        with bd.cursor as cursor:
            cursor.execute(consulta)
            result = cursor.fetchall()
            if result:
                resultados_dict = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
                return resultados_dict
            else:
                return None
    except Exception as e:
        print(e)
    finally:
        bd.conn.close()

#Viviendas
def listarViviendas():
    bd = BD()
    bd.connect()
    consulta = "SELECT v.*, (SELECT COUNT(*) FROM clientes c WHERE c.direccion = v.nombre ) as habitantes FROM viviendas v"
    try:
        with bd.cursor as cursor:
            cursor.execute(consulta)
            result = cursor.fetchall()
            if result:
                resultados_dict = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
                return resultados_dict
            else:
                return None
    except Exception as e:
        print(e)
    finally:
        bd.conn.close()

def guardarVivienda(nombre, imagen, location):
    bd = BD()
    bd.connect()
    consulta = "INSERT INTO viviendas(nombre, imagen, locacion) VALUES (%s, %s, %s)"
    try:
        with bd.cursor as cursor:
            cursor.execute(consulta, (nombre, imagen, location))
            bd.conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(e)
    finally:
        bd.conn.close()

def eliminarVivienda(id):
    bd=BD()
    bd.connect()
    consulta = "DELETE FROM viviendas WHERE id = %s"
    try:
        with bd.cursor as cursor:
            cursor.execute(consulta, (id))
            bd.conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(e)
    finally:
        bd.conn.close()

#usuario
def buscarUsuario(usuario):
    bd = BD()
    bd.connect()
    consulta = "SELECT * FROM usuarios WHERE usuario = %s"
    try:
        with bd.cursor as cursor:
            cursor.execute(consulta, (usuario))
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None
    except Exception as e:
        print(e)
    finally:
        bd.conn.close()

#habitantes
def listarHabitantes():
    bd = BD()
    bd.connect()
    consulta = "SELECT * FROM clientes"
    try:
        with bd.cursor as cursor:
            cursor.execute(consulta)
            result = cursor.fetchall()
            if result:
                resultados_dict = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
                return resultados_dict
            else:
                return None
    except Exception as e:
        print(e)
    finally:
        bd.conn.close()

# Agregar habitante
def guardarHabitante(nombre, sexo, direccion, telefono, ciudad):
    bd = BD()
    bd.connect()
    consulta = "INSERT INTO clientes(nombre, sexo, direccion, telefono, ciudad) VALUES (%s, %s, %s, %s, %s)"
    try:
        with bd.cursor as cursor:
            cursor.execute(consulta, (nombre, sexo, direccion, telefono, ciudad))
            bd.conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(e)
    finally:
        bd.conn.close()

# Eliminar habitante por ID
def eliminarHabitante(id):
    bd = BD()
    bd.connect()
    consulta = "DELETE FROM clientes WHERE id = %s"
    try:
        with bd.cursor as cursor:
            cursor.execute(consulta, (id,))
            bd.conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(e)
    finally:
        bd.conn.close()