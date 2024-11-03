import tkinter as tk
from tkinter import ttk
from gui.interfaz_registro_auto import InterfazRegistroAuto
from gui.interfaz_registro_cliente import InterfazRegistroCliente
from gui.interfaz_registro_venta import InterfazRegistroVenta
from gui.interfaz_registro_servicio import InterfazRegistroServicio
from gui.interfaz_registro_vendedor import InterfazRegistroVendedor
from gui.interfaz_consulta_autos_vendidos import InterfazConsultaAutosVendidos

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Concesionaria de Autos")

        # Crear estilo
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TEntry", padding=5)

        # Crear el contenedor principal
        self.contenedor = ttk.Notebook(root)
        self.contenedor.pack(expand=1, fill='both')

        # Crear las diferentes páginas
        self.frame_auto = InterfazRegistroAuto(self.contenedor)
        self.frame_cliente = InterfazRegistroCliente(self.contenedor)
        self.frame_venta = InterfazRegistroVenta(self.contenedor)
        self.frame_servicio = InterfazRegistroServicio(self.contenedor)
        self.frame_vendedor = InterfazRegistroVendedor(self.contenedor)
        self.frame_autos_vendidos = InterfazConsultaAutosVendidos(self.contenedor)

        # Agregar las páginas al contenedor
        self.contenedor.add(self.frame_auto, text="Registrar Auto")
        self.contenedor.add(self.frame_cliente, text="Registrar Cliente")
        self.contenedor.add(self.frame_vendedor, text="Registrar Vendedor")
        self.contenedor.add(self.frame_venta, text="Registrar Venta")
        self.contenedor.add(self.frame_servicio, text="Registrar Servicio")
        self.contenedor.add(self.frame_autos_vendidos, text="Consultar Autos")
        
