import tkinter as tk
from tkinter import ttk, messagebox
from base_de_datos import BaseDatos

class SistemaEventos:
    def __init__(self):
        self.db = BaseDatos()
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Gestión de Eventos Universitarios")
        self.ventana.geometry("800x600")
        
        self.usuario_actual = None
        self.mostrar_login()

    def mostrar_login(self):
        # Limpiar ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()

        # Crear frame de login
        frame_login = ttk.Frame(self.ventana, padding="20")
        frame_login.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Elementos del login
        ttk.Label(frame_login, text="Correo:").grid(row=0, column=0, pady=5)
        self.correo = ttk.Entry(frame_login)
        self.correo.grid(row=0, column=1, pady=5)

        ttk.Label(frame_login, text="Contraseña:").grid(row=1, column=0, pady=5)
        self.contrasena = ttk.Entry(frame_login, show="*")
        self.contrasena.grid(row=1, column=1, pady=5)

        ttk.Button(frame_login, text="Iniciar Sesión", 
                  command=self.iniciar_sesion).grid(row=2, column=0, columnspan=2, pady=10)

    def iniciar_sesion(self):
        correo = self.correo.get()
        password = self.contrasena.get()
        
        try:
            cursor = self.db.conexion.cursor()
            query = "SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s"
            cursor.execute(query, (correo, password))
            usuario = cursor.fetchone()
            
            if usuario:
                self.usuario_actual = {
                    'id': usuario[0],
                    'nombre': usuario[1],
                    'correo': usuario[2],
                    'rol': usuario[4]
                }
                messagebox.showinfo("Éxito", f"Bienvenido {usuario[1]}")
                # Aquí puedes agregar la lógica para mostrar la siguiente pantalla
                # self.mostrar_pantalla_principal()
            else:
                messagebox.showerror("Error", "Credenciales inválidas")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {e}")
        finally:
            cursor.close()

    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = SistemaEventos()
    app.ejecutar()
