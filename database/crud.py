import sqlite3

# Registrar auto - LISTO
def registrar_auto(vin, marca, modelo, anio, precio, estado):
    try:
        conn = sqlite3.connect('concesionaria.db')  # Asegúrate de que la ruta sea correcta
        cursor = conn.cursor()
        
        # Comprobar si el auto ya existe
        cursor.execute("SELECT * FROM autos WHERE vin = ?", (vin,))
        if cursor.fetchone() is not None:
            return False  # Indica que el auto ya existe
        
        cursor.execute("INSERT INTO autos (vin, marca, modelo, anio, precio, estado) VALUES (?, ?, ?, ?, ?, ?)",
                       (vin, marca, modelo, anio, precio, estado))
        conn.commit()
        return True  # Retorna True si la inserción es exitosa
    except Exception as e:
        print(f"Error al registrar el auto: {e}")  # Puedes ver el error en la consola
        return False  # Retorna False si hay un error
    finally:
        conn.close()

# Registrar cliente - LISTO
def registrar_cliente(nombre, apellido, direccion, telefono):
    try:
        conn = sqlite3.connect('concesionaria.db')  # Asegúrate de que la ruta sea correcta
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nombre, apellido, direccion, telefono) VALUES (?, ?, ?, ?)",
                       (nombre, apellido, direccion, telefono))
        conn.commit()
        return True  # Retorna True si la inserción es exitosa
    except Exception as e:
        print(f"Error al registrar el cliente: {e}")  # Puedes ver el error en la consola
        return False  # Retorna False si hay un error
    finally:
        conn.close()
        
# Registrar vendedor- LISTO
def registrar_vendedor(nombre, apellido, comisiones=0):
    try:
        conn = sqlite3.connect('concesionaria.db')  # Asegúrate de que la ruta sea correcta
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vendedores (nombre, apellido, comisiones) VALUES (?, ?, ?)",
                       (nombre, apellido, comisiones))
        conn.commit()
        return True  # Retorna True si la inserción es exitosa
    except Exception as e:
        print(f"Error al registrar vendedor: {e}")  # Puedes ver el error en la consola
        return False  # Retorna False si hay un error
    finally:
        conn.close()


# Registrar venta
def registrar_venta(vin, cliente_id, fecha_venta, vendedor_id, comision):
    try:
        conn = sqlite3.connect('concesionaria.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ventas (vin, cliente_id, fecha_venta, vendedor_id) VALUES (?, ?, ?, ?)",
                    (vin, cliente_id, fecha_venta, vendedor_id))
        cursor.execute("UPDATE autos SET cliente_id = ? WHERE vin = ?", (cliente_id, vin))
        
        # Insertar la comisión en la tabla de comisiones
        cursor.execute("INSERT INTO comisiones (vendedor_id, monto, fecha) VALUES (?, ?, ?)", (vendedor_id, comision, fecha_venta))
    
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al registrar venta: {e}")  # Puedes ver el error en la consola
        return False  # Retorna False si hay un error
    finally:
        conn.close()
        
    
# Obtener autos aún no vendidos que esten disponibles para la venta
def obtener_autos_no_vendidos():
    conn = sqlite3.connect('concesionaria.db')
    cursor = conn.cursor()
    # Cambiar la condición a cliente_id IS NULL para obtener autos no vendidos
    cursor.execute("SELECT vin, marca, modelo FROM autos WHERE cliente_id IS NULL")
    autos_no_vendidos = cursor.fetchall()
    conn.close()
    return autos_no_vendidos


# Registrar servicio
def registrar_servicio(vin, tipo_servicio, fecha, costo):
    try:
        conn = sqlite3.connect('concesionaria.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO servicios (vin, tipo_servicio, fecha, costo) VALUES (?, ?, ?, ?)",
                    (vin, tipo_servicio, fecha, costo))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al registrar servicio: {e}")  # Puedes ver el error en la consola
        return False  # Retorna False si hay un error
    finally:
        conn.close()


# Obtener datos de un auto vendido por un cliente
def obtener_autos_vendidos_por_cliente(cliente_id):
    conn = sqlite3.connect("concesionaria.db")
    cursor = conn.cursor()
    cursor.execute("SELECT vin, marca, modelo, anio, precio, estado FROM autos WHERE cliente_id = ?", (cliente_id,))
    autos = cursor.fetchall()
    conn.close()
    return autos

# Consultar servicios de un auto específico
def consultar_servicios(vin):
    conn = sqlite3.connect('concesionaria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicios WHERE vin = ?", (vin,))
    servicios = cursor.fetchall()
    conn.close()
    return servicios


# Obtener autos vendidos (con cliente asignado)
def obtener_autos_vendidos():
    conn = sqlite3.connect('concesionaria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT vin, marca, modelo FROM autos WHERE cliente_id IS NOT NULL")
    autos_vendidos = cursor.fetchall()
    conn.close()
    return autos_vendidos


# Obtener lista de clientes
def obtener_clientes():
    conn = sqlite3.connect('concesionaria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nombre, apellido FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

# Obtener lista de vendedores
def obtener_vendedores():
    conn = sqlite3.connect('concesionaria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_vendedor, nombre, apellido FROM vendedores")
    vendedores = cursor.fetchall()
    conn.close()
    return vendedores
















# Consultar servicios realizados a un auto específico
def consultar_servicios_auto(vin):
    conn = sqlite3.connect('concesionaria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT tipo_servicio, fecha, costo FROM servicios WHERE vin = ?", (vin,))
    servicios = cursor.fetchall()
    conn.close()
    return servicios

import sqlite3

