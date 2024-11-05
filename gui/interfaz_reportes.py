import tkinter as tk
from tkinter import ttk
from database.database_connection import DatabaseConnection
from tkinter import simpledialog
import tkinter.messagebox as messagebox

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

        # Inicializar las etiquetas para mostrar los totales, pero no las configuramos aún
        self.label_ventas = ttk.Label(self, text="Total Ventas:")
        self.total_ventas = ttk.Label(self, text="$0.00")  # Widget para mostrar total de ventas
        self.label_servicios = ttk.Label(self, text="Total Servicios:")
        self.total_servicios = ttk.Label(self, text="$0.00")  # Widget para mostrar total de servicios
        # Inicializar el estado de visibilidad
        self.ventas_visible = False
        
        # Inicializar las etiquetas para mostrar los autos más vendidos
        self.label_autos_mas_vendidos = ttk.Label(self, text="Autos más vendidos por marca:")
        self.autos_mas_vendidos_frame = ttk.Frame(self)  # Contenedor para los resultados
        self.autos_mas_vendidos_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky='w')
        # Esta variable controlará la visibilidad del contenedor
        self.autos_visible = False

    def listado_ventas_por_periodo(self):
        # Aquí implementas la lógica para mostrar el listado de ventas por periodo
        print("Listado de ventas por periodo")
        # Crear un cuadro de diálogo para ingresar las fechas
        fecha_inicio = simpledialog.askstring("Fecha de inicio", "Ingrese la fecha de inicio (DD/MM/AAAA):")
        fecha_fin = simpledialog.askstring("Fecha de fin", "Ingrese la fecha de fin (DD/MM/AAAA):")

        # Validar las fechas ingresadas
        if not fecha_inicio or not fecha_fin:
            messagebox.showwarning("Advertencia", "Ambas fechas son obligatorias.")
            return

        # Conectar a la base de datos
        db = DatabaseConnection()
        cursor = db.get_connection().cursor()

        # Realizar la consulta
        try:
            # La consulta se realiza en el formato correcto para SQLite
            cursor.execute("""
                SELECT id_venta, vin, cliente_id, fecha_venta, vendedor_id
                FROM ventas
                WHERE fecha_venta BETWEEN ? AND ?
            """, (fecha_inicio, fecha_fin))

            resultados = cursor.fetchall()

            # Verificar si se encontraron resultados
            if resultados:
                # Crear una nueva ventana para mostrar los resultados
                ventana_resultados = tk.Toplevel(self)
                ventana_resultados.title("Resultados de Ventas")
                
                # Títulos de las columnas
                ttk.Label(ventana_resultados, text="ID Venta").grid(row=0, column=0)
                ttk.Label(ventana_resultados, text="VIN").grid(row=0, column=1)
                ttk.Label(ventana_resultados, text="Cliente ID").grid(row=0, column=2)
                ttk.Label(ventana_resultados, text="Fecha Venta").grid(row=0, column=3)
                ttk.Label(ventana_resultados, text="Vendedor ID").grid(row=0, column=4)

                # Crear tabla
                for idx, (id_venta, vin, cliente_id, fecha_venta, vendedor_id) in enumerate(resultados, start=1):
                    ttk.Label(ventana_resultados, text=f"{id_venta}").grid(row=idx, column=0)
                    ttk.Label(ventana_resultados, text=f"{vin}").grid(row=idx, column=1)
                    ttk.Label(ventana_resultados, text=f"{cliente_id}").grid(row=idx, column=2)
                    ttk.Label(ventana_resultados, text=f"{fecha_venta}").grid(row=idx, column=3)
                    ttk.Label(ventana_resultados, text=f"{vendedor_id}").grid(row=idx, column=4)
            else:
                messagebox.showinfo("Información", "No se encontraron ventas en el rango de fechas especificado.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()

    def ingresos_totales(self):
        db = DatabaseConnection()  # Crear conexión a la base de datos
        cursor = db.get_connection().cursor()

        ## VER SI ESTE CALCULO ESTA BIEN O SERIA LA SUMA DE LAS COMISIONES DE LOS VENDEDORES
        # Calcular el total de ventas sumando el precio de los autos relacionados con las ventas
        cursor.execute("""
            SELECT SUM(a.precio) 
            FROM ventas v 
            JOIN autos a ON v.vin = a.vin
        """)
        total_ventas = cursor.fetchone()[0] or 0  # Manejar caso de NULL

        # Calcular el total de servicios
        cursor.execute("SELECT SUM(costo) FROM servicios")
        total_servicios = cursor.fetchone()[0] or 0  # Manejar caso de NULL

        # Mostrar los resultados
        self.total_ventas.config(text=f"${total_ventas:.2f}")
        self.total_servicios.config(text=f"${total_servicios:.2f}")

        # Empaquetar las etiquetas solo cuando se genera el reporte
        if not self.ventas_visible:
            # Colocar las etiquetas en la cuadrícula
            self.label_ventas.grid(row=4, column=0, pady=10, sticky='w')
            self.total_ventas.grid(row=4, column=1, pady=10, sticky='w')
            self.label_servicios.grid(row=5, column=0, pady=10, sticky='w')
            self.total_servicios.grid(row=5, column=1, pady=10, sticky='w')
            self.ventas_visible = True  # Marcar que las etiquetas ya se mostraron

    def autos_mas_vendidos(self):
        # Aquí implementas la lógica para mostrar los autos más vendidos por marca
        print("Autos más vendidos por marca")
        db = DatabaseConnection()
        cursor = db.get_connection().cursor()

        # Consulta para obtener el total de ventas por modelo y marca
        cursor.execute("""
            SELECT a.marca, a.modelo, COUNT(v.id_venta) AS total_ventas
            FROM autos a
            JOIN ventas v ON a.vin = v.vin
            GROUP BY a.marca, a.modelo
            ORDER BY a.marca, total_ventas DESC;
        """)
        
        resultados = cursor.fetchall()

        # Limpiar resultados anteriores
        for widget in self.autos_mas_vendidos_frame.winfo_children():
            widget.destroy()

        # Crear un diccionario para almacenar el modelo más vendido por marca
        autos_mas_vendidos = {}
        for marca, modelo, total in resultados:
            if marca not in autos_mas_vendidos:
                autos_mas_vendidos[marca] = (modelo, total)

        # Mostrar los resultados solo cuando se genera el reporte
        if not self.autos_visible:
            self.label_autos_mas_vendidos.grid(row=4, column=0, sticky='w')
            self.autos_visible = True

        # Colocar los resultados en el contenedor
        for idx, (marca, (modelo, total)) in enumerate(autos_mas_vendidos.items()):
            ttk.Label(self.autos_mas_vendidos_frame, text=f"Marca: {marca}, Modelo: {modelo}, Ventas: {total}").grid(row=idx, column=0, sticky='w')
        

