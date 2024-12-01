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
                self.mostrar_pantalla_principal()
            else:
                messagebox.showerror("Error", "Credenciales inválidas")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {e}")
        finally:
            cursor.close()

    def mostrar_pantalla_principal(self):
        # Limpiar ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()

        # Frame principal
        frame_principal = ttk.Frame(self.ventana, padding="20")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        ttk.Label(frame_principal, 
                 text=f"Bienvenido al Sistema de Eventos - {self.usuario_actual['nombre']}", 
                 font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Botones según el rol
        if self.usuario_actual['rol'] == 'administrador':
            ttk.Button(frame_principal, text="Gestionar Eventos", 
                      command=self.mostrar_gestion_eventos).grid(row=1, column=0, pady=5)
            ttk.Button(frame_principal, text="Gestionar Usuarios", 
                      command=self.mostrar_gestion_usuarios).grid(row=2, column=0, pady=5)
        else:
            ttk.Button(frame_principal, text="Ver Eventos Disponibles", 
                      command=self.mostrar_eventos_disponibles).grid(row=1, column=0, pady=5)
            ttk.Button(frame_principal, text="Mis Inscripciones", 
                      command=self.mostrar_mis_inscripciones).grid(row=2, column=0, pady=5)

        # Botón de cerrar sesión
        ttk.Button(frame_principal, text="Cerrar Sesión", 
                  command=self.mostrar_login).grid(row=3, column=0, pady=20)

    def ejecutar(self):
        self.ventana.mainloop()

    def mostrar_gestion_eventos(self):
        # Limpiar ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()

        # Frame principal
        frame_eventos = ttk.Frame(self.ventana, padding="20")
        frame_eventos.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        ttk.Label(frame_eventos, text="Gestión de Eventos", 
                 font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Frame para crear eventos
        frame_crear = ttk.LabelFrame(frame_eventos, text="Crear Nuevo Evento", padding="10")
        frame_crear.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Campos para nuevo evento
        ttk.Label(frame_crear, text="Título:").grid(row=0, column=0, pady=5)
        self.titulo_evento = ttk.Entry(frame_crear)
        self.titulo_evento.grid(row=0, column=1, pady=5)

        ttk.Label(frame_crear, text="Descripción:").grid(row=1, column=0, pady=5)
        self.descripcion_evento = ttk.Entry(frame_crear)
        self.descripcion_evento.grid(row=1, column=1, pady=5)

        ttk.Label(frame_crear, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, pady=5)
        self.fecha_evento = ttk.Entry(frame_crear)
        self.fecha_evento.grid(row=2, column=1, pady=5)

        ttk.Label(frame_crear, text="Hora (HH:MM):").grid(row=3, column=0, pady=5)
        self.hora_evento = ttk.Entry(frame_crear)
        self.hora_evento.grid(row=3, column=1, pady=5)

        ttk.Label(frame_crear, text="Lugar:").grid(row=4, column=0, pady=5)
        self.lugar_evento = ttk.Entry(frame_crear)
        self.lugar_evento.grid(row=4, column=1, pady=5)

        ttk.Label(frame_crear, text="Categoría:").grid(row=5, column=0, pady=5)
        self.categoria_evento = ttk.Entry(frame_crear)
        self.categoria_evento.grid(row=5, column=1, pady=5)

        ttk.Button(frame_crear, text="Crear Evento", 
                  command=self.crear_evento).grid(row=6, column=0, columnspan=2, pady=10)

        # Lista de eventos existentes
        frame_lista = ttk.LabelFrame(frame_eventos, text="Eventos Existentes", padding="10")
        frame_lista.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Botón para actualizar lista
        ttk.Button(frame_lista, text="Actualizar Lista", 
                  command=self.actualizar_lista_eventos).grid(row=0, column=0, pady=5)

        # TreeView para mostrar eventos
        self.tree_eventos = ttk.Treeview(frame_lista, columns=('ID', 'Título', 'Fecha', 'Lugar'), 
                                       show='headings')
        self.tree_eventos.heading('ID', text='ID')
        self.tree_eventos.heading('Título', text='Título')
        self.tree_eventos.heading('Fecha', text='Fecha')
        self.tree_eventos.heading('Lugar', text='Lugar')
        self.tree_eventos.grid(row=1, column=0, pady=5)

        # Botón para eliminar evento seleccionado
        ttk.Button(frame_lista, text="Eliminar Evento Seleccionado", 
                  command=self.eliminar_evento).grid(row=2, column=0, pady=5)

        # Botón para volver
        ttk.Button(frame_eventos, text="Volver", 
                  command=self.mostrar_pantalla_principal).grid(row=2, column=0, columnspan=2, pady=20)

        # Cargar eventos existentes
        self.actualizar_lista_eventos()

    def crear_evento(self):
        try:
            cursor = self.db.conexion.cursor()
            query = """
                INSERT INTO eventos (titulo, descripcion, fecha, hora, lugar, categoria, administrador_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                self.titulo_evento.get(),
                self.descripcion_evento.get(),
                self.fecha_evento.get(),
                self.hora_evento.get(),
                self.lugar_evento.get(),
                self.categoria_evento.get(),
                self.usuario_actual['id']
            )
            cursor.execute(query, valores)
            self.db.conexion.commit()
            messagebox.showinfo("Éxito", "Evento creado exitosamente")
            self.actualizar_lista_eventos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear evento: {e}")
        finally:
            cursor.close()

    def actualizar_lista_eventos(self):
        # Limpiar lista actual
        for item in self.tree_eventos.get_children():
            self.tree_eventos.delete(item)
        
        try:
            cursor = self.db.conexion.cursor()
            cursor.execute("SELECT id, titulo, fecha, lugar FROM eventos")
            for evento in cursor.fetchall():
                self.tree_eventos.insert('', 'end', values=evento)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar eventos: {e}")
        finally:
            cursor.close()

    def eliminar_evento(self):
        seleccion = self.tree_eventos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un evento para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el evento seleccionado?"):
            try:
                evento_id = self.tree_eventos.item(seleccion[0])['values'][0]
                cursor = self.db.conexion.cursor()
                cursor.execute("DELETE FROM eventos WHERE id = %s", (evento_id,))
                self.db.conexion.commit()
                messagebox.showinfo("Éxito", "Evento eliminado exitosamente")
                self.actualizar_lista_eventos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar evento: {e}")
            finally:
                cursor.close()

    def mostrar_gestion_usuarios(self):
        # Limpiar ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()

        # Frame principal
        frame_usuarios = ttk.Frame(self.ventana, padding="20")
        frame_usuarios.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        ttk.Label(frame_usuarios, text="Gestión de Usuarios", 
                 font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Frame para crear usuarios
        frame_crear = ttk.LabelFrame(frame_usuarios, text="Crear Nuevo Usuario", padding="10")
        frame_crear.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Campos para nuevo usuario
        ttk.Label(frame_crear, text="Nombre:").grid(row=0, column=0, pady=5)
        self.nombre_usuario = ttk.Entry(frame_crear)
        self.nombre_usuario.grid(row=0, column=1, pady=5)

        ttk.Label(frame_crear, text="Correo:").grid(row=1, column=0, pady=5)
        self.correo_usuario = ttk.Entry(frame_crear)
        self.correo_usuario.grid(row=1, column=1, pady=5)

        ttk.Label(frame_crear, text="Contraseña:").grid(row=2, column=0, pady=5)
        self.contrasena_usuario = ttk.Entry(frame_crear, show="*")
        self.contrasena_usuario.grid(row=2, column=1, pady=5)

        ttk.Label(frame_crear, text="Rol:").grid(row=3, column=0, pady=5)
        self.rol_usuario = ttk.Combobox(frame_crear, values=['estudiante', 'administrador'])
        self.rol_usuario.set('estudiante')
        self.rol_usuario.grid(row=3, column=1, pady=5)

        ttk.Button(frame_crear, text="Crear Usuario", 
                  command=self.crear_usuario).grid(row=4, column=0, columnspan=2, pady=10)

        # Lista de usuarios existentes
        frame_lista = ttk.LabelFrame(frame_usuarios, text="Usuarios Existentes", padding="10")
        frame_lista.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        # TreeView para mostrar usuarios
        self.tree_usuarios = ttk.Treeview(frame_lista, 
                                        columns=('ID', 'Nombre', 'Correo', 'Rol'), 
                                        show='headings')
        self.tree_usuarios.heading('ID', text='ID')
        self.tree_usuarios.heading('Nombre', text='Nombre')
        self.tree_usuarios.heading('Correo', text='Correo')
        self.tree_usuarios.heading('Rol', text='Rol')
        self.tree_usuarios.grid(row=0, column=0, pady=5)

        # Botón para eliminar usuario seleccionado
        ttk.Button(frame_lista, text="Eliminar Usuario", 
                  command=self.eliminar_usuario).grid(row=1, column=0, pady=5)

        # Botón para volver
        ttk.Button(frame_usuarios, text="Volver", 
                  command=self.mostrar_pantalla_principal).grid(row=2, column=0, columnspan=2, pady=20)

        # Cargar usuarios existentes
        self.actualizar_lista_usuarios()

    def crear_usuario(self):
        try:
            cursor = self.db.conexion.cursor()
            query = """
                INSERT INTO usuarios (nombre, correo, contrasena, rol)
                VALUES (%s, %s, %s, %s)
            """
            valores = (
                self.nombre_usuario.get(),
                self.correo_usuario.get(),
                self.contrasena_usuario.get(),
                self.rol_usuario.get()
            )
            cursor.execute(query, valores)
            self.db.conexion.commit()
            messagebox.showinfo("Éxito", "Usuario creado exitosamente")
            self.actualizar_lista_usuarios()
            
            # Limpiar campos
            self.nombre_usuario.delete(0, tk.END)
            self.correo_usuario.delete(0, tk.END)
            self.contrasena_usuario.delete(0, tk.END)
            self.rol_usuario.set('estudiante')
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear usuario: {e}")
        finally:
            cursor.close()

    def actualizar_lista_usuarios(self):
        # Limpiar lista actual
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        try:
            cursor = self.db.conexion.cursor()
            cursor.execute("SELECT id, nombre, correo, rol FROM usuarios")
            for usuario in cursor.fetchall():
                self.tree_usuarios.insert('', 'end', values=usuario)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {e}")
        finally:
            cursor.close()

    def eliminar_usuario(self):
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el usuario seleccionado?"):
            try:
                usuario_id = self.tree_usuarios.item(seleccion[0])['values'][0]
                cursor = self.db.conexion.cursor()
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
                self.db.conexion.commit()
                messagebox.showinfo("Éxito", "Usuario eliminado exitosamente")
                self.actualizar_lista_usuarios()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar usuario: {e}")
            finally:
                cursor.close()

if __name__ == "__main__":
    app = SistemaEventos()
    app.ejecutar()
