class Auto:
    def __init__(self, vin, marca, modelo, anio, precio, estado, cliente=None):
        self.vin = vin
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.precio = precio
        self.estado = estado
        self.cliente = cliente
