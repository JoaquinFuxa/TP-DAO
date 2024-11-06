import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from database.database_connection import DatabaseConnection
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class InterfazReportes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configuración de estilo para los botones
        estilo = ttk.Style()
        estilo.configure("TButton", padding=10, font=("Arial", 10, "bold"))

        # Título de la interfaz
        ttk.Label(self, text="Consultas de Reportes", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Botón para "Listado de ventas por periodo" - Genera PDF
        self.boton_listado_ventas = ttk.Button(self, text="Listado de ventas por periodo (PDF)", command=self.listado_ventas_por_periodo)
        self.boton_listado_ventas.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Botón para "Ingresos totales por venta de autos y servicios" - Genera PDF
        self.boton_ingresos_totales = ttk.Button(self, text="Ingresos totales (PDF)", command=self.ingresos_totales)
        self.boton_ingresos_totales.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Botón para "Autos más vendidos por marca" - Genera PDF
        self.boton_autos_mas_vendidos = ttk.Button(self, text="Autos más vendidos por marca (PDF)", command=self.autos_mas_vendidos)
        self.boton_autos_mas_vendidos.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)


    def listado_ventas_por_periodo(self):
        fecha_inicio = simpledialog.askstring("Fecha de inicio", "Ingrese la fecha de inicio (DD/MM/AAAA):")
        fecha_fin = simpledialog.askstring("Fecha de fin", "Ingrese la fecha de fin (DD/MM/AAAA):")
        
        if not fecha_inicio or not fecha_fin:
            messagebox.showwarning("Advertencia", "Ambas fechas son obligatorias.")
            return

        db = DatabaseConnection()
        cursor = db.get_connection().cursor()
        
        try:
            cursor.execute("""
                SELECT id_venta, vin, cliente_id, fecha_venta, vendedor_id
                FROM ventas
                WHERE strftime('%Y-%m-%d', fecha_venta) BETWEEN strftime('%Y-%m-%d', ?) AND strftime('%Y-%m-%d', ?)
            """, (fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()
            
            # Crear PDF
            pdf = canvas.Canvas("reporte_ventas_por_periodo.pdf", pagesize=A4)
            pdf.drawString(100, 800, f"Listado de Ventas del {fecha_inicio} al {fecha_fin}")
            
            y_position = 750
            pdf.drawString(50, y_position, "ID Venta")
            pdf.drawString(120, y_position, "VIN")
            pdf.drawString(250, y_position, "Cliente ID")
            pdf.drawString(370, y_position, "Fecha Venta")
            pdf.drawString(500, y_position, "Vendedor ID")

            y_position -= 20
            for id_venta, vin, cliente_id, fecha_venta, vendedor_id in resultados:
                pdf.drawString(50, y_position, str(id_venta))
                pdf.drawString(100, y_position, vin)
                pdf.drawString(150, y_position, str(cliente_id))
                pdf.drawString(200, y_position, fecha_venta)
                pdf.drawString(250, y_position, str(vendedor_id))
                y_position -= 20

            pdf.save()
            messagebox.showinfo("Reporte generado", "El reporte de ventas se ha guardado como PDF.")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()

    def ingresos_totales(self):
        db = DatabaseConnection()
        cursor = db.get_connection().cursor()
        
        try:
            cursor.execute("SELECT SUM(a.precio) FROM ventas v JOIN autos a ON v.vin = a.vin")
            total_ventas = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(costo) FROM servicios")
            total_servicios = cursor.fetchone()[0] or 0
            
            # Crear PDF
            pdf = canvas.Canvas("reporte_ingresos_totales.pdf", pagesize=A4)
            pdf.drawString(100, 800, "Ingresos Totales")
            pdf.drawString(100, 750, f"Total Ventas: ${total_ventas:.2f}")
            pdf.drawString(100, 730, f"Total Servicios: ${total_servicios:.2f}")
            pdf.save()
            messagebox.showinfo("Reporte generado", "El reporte de ingresos totales se ha guardado como PDF.")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()

    def autos_mas_vendidos(self):
        db = DatabaseConnection()
        cursor = db.get_connection().cursor()

        try:
            cursor.execute("""
                SELECT a.marca, a.modelo, COUNT(v.id_venta) AS total_ventas
                FROM autos a
                JOIN ventas v ON a.vin = v.vin
                GROUP BY a.marca, a.modelo
                ORDER BY a.marca, total_ventas DESC;
            """)
            resultados = cursor.fetchall()
            
            pdf = canvas.Canvas("reporte_autos_mas_vendidos.pdf", pagesize=A4)
            pdf.drawString(100, 800, "Autos Más Vendidos por Marca")
            y_position = 750
            
            for marca, modelo, total_ventas in resultados:
                pdf.drawString(50, y_position, f"{marca} - {modelo}: {total_ventas} ventas")
                y_position -= 20

            pdf.save()
            messagebox.showinfo("Reporte generado", "El reporte de autos más vendidos se ha guardado como PDF.")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
