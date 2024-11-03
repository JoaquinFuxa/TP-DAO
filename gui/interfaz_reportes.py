import tkinter as tk
from tkinter import ttk

class InterfazReportes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configuración de estilo para los botones
        estilo = ttk.Style()
        estilo.configure("TButton", padding=10, font=("Arial", 10, "bold"))

        # Título de la interfaz
        ttk.Label(self, text="Consultas de Reportes", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Botón para "Listado de ventas por periodo"
        self.boton_listado_ventas = ttk.Button(self, text="Listado de ventas por periodo", command=self.listado_ventas_por_periodo)
        self.boton_listado_ventas.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Botón para "Ingresos totales por venta de autos y servicios"
        self.boton_ingresos_totales = ttk.Button(self, text="Ingresos totales por venta de autos y servicios", command=self.ingresos_totales)
        self.boton_ingresos_totales.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Botón para "Autos más vendidos por marca"
        self.boton_autos_mas_vendidos = ttk.Button(self, text="Autos más vendidos por marca", command=self.autos_mas_vendidos)
        self.boton_autos_mas_vendidos.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    def listado_ventas_por_periodo(self):
        # Aquí implementas la lógica para mostrar el listado de ventas por periodo
        print("Listado de ventas por periodo")

    def ingresos_totales(self):
        # Aquí implementas la lógica para calcular y mostrar los ingresos totales
        print("Ingresos totales por venta de autos y servicios")

    def autos_mas_vendidos(self):
        # Aquí implementas la lógica para mostrar los autos más vendidos por marca
        print("Autos más vendidos por marca")

