from .database_connection import DatabaseConnection  # Importa DatabaseConnection

def crear_base_de_datos():
    db = DatabaseConnection()
    cursor = db.get_connection().cursor()

    # Crear tabla autos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS autos (
            vin TEXT PRIMARY KEY,
            marca TEXT,
            modelo TEXT,
            anio INTEGER,
            precio REAL,
            estado TEXT,
            cliente_id INTEGER,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id_cliente)
        )
    ''')

    # Crear tabla clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            direccion TEXT,
            telefono TEXT
        )
    ''')

    # Crear tabla ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            vin TEXT,
            cliente_id INTEGER,
            fecha_venta DATE,
            vendedor_id INTEGER,
            FOREIGN KEY(vin) REFERENCES autos(vin),
            FOREIGN KEY(cliente_id) REFERENCES clientes(id_cliente),
            FOREIGN KEY(vendedor_id) REFERENCES vendedores(id_vendedor)
        )
    ''')

    # Crear tabla servicios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicios (
            id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
            vin TEXT,
            tipo_servicio TEXT,
            fecha DATE,
            costo REAL,
            FOREIGN KEY(vin) REFERENCES autos(vin)
        )
    ''')

    # Crear tabla vendedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendedores (
            id_vendedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            comisiones REAL
        )
    ''')
    
    # Crear tabla comisiones para almacenar las comisiones de las ventas
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS comisiones ( 
            id_comision INTEGER PRIMARY KEY AUTOINCREMENT, 
            vendedor_id INTEGER, 
            monto REAL, 
            fecha DATE, 
            FOREIGN KEY(vendedor_id) REFERENCES vendedores(id_vendedor) 
        ) 
    ''')


    db.get_connection().commit()
    #onn.commit()
    #conn.close()

def cargar_datos_mock():
    db = DatabaseConnection()
    cursor = db.get_connection().cursor()

    # Verificar si ya hay datos en la tabla clientes
    cursor.execute('SELECT COUNT(*) FROM clientes')
    if cursor.fetchone()[0] == 0:  # Si la tabla está vacía, insertar clientes
        clientes = [
            ('Joaquin', 'Fuxa', 'Calle Falsa 123', '123456789'),
            ('Maria', 'Lopez', 'Avenida Siempre Viva 742', '987654321'),
            ('Pedro', 'Gomez', 'Boulevard de los sueños 999', '456123789')
        ]
        cursor.executemany('INSERT INTO clientes (nombre, apellido, direccion, telefono) VALUES (?, ?, ?, ?)', clientes)

    # Verificar si ya hay datos en la tabla vendedores
    cursor.execute('SELECT COUNT(*) FROM vendedores')
    if cursor.fetchone()[0] == 0:  # Si la tabla está vacía, insertar vendedores
        vendedores = [
            ('Carlos', 'Sanchez', 5000),
            ('Ana', 'Martinez', 7000),
            ('Luis', 'Fernandez', 6000)
        ]
        cursor.executemany('INSERT INTO vendedores (nombre, apellido, comisiones) VALUES (?, ?, ?)', vendedores)

    # Verificar si ya hay datos en la tabla autos
    cursor.execute('SELECT COUNT(*) FROM autos')
    if cursor.fetchone()[0] == 0:  # Si la tabla está vacía, insertar autos
        autos = [
            ('AAA', 'Honda', 'Accord', 2020, 25000.00, 'nuevo'),
            ('BBB', 'Ford', 'Mustang', 2021, 35000.00, 'nuevo'),
            ('CCC', 'Nissan', 'Altima', 2019, 22000.00, 'usado'),
            ('EEE', 'Nissan', 'Altima', 2019, 22000.00, 'usado'),
            ('DDD', 'Nissan', 'Altima', 2019, 22000.00, 'usado')
        ]
        cursor.executemany('INSERT INTO autos (vin, marca, modelo, anio, precio, estado) VALUES (?, ?, ?, ?, ?, ?)', autos)

    db.get_connection().commit()

# Crear la base de datos
crear_base_de_datos()

# Cargar datos de prueba
cargar_datos_mock()
