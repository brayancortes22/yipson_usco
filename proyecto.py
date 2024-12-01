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

        # Frame de login
        frame_login = ttk.Frame(self.ventana, padding="20")
        frame_login.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        ttk.Label(frame_login, text="Sistema de Gestión de Eventos", 
                 font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos de login
        ttk.Label(frame_login, text="Correo:").grid(row=1, column=0, pady=5)
        self.correo = ttk.Entry(frame_login)
        self.correo.grid(row=1, column=1, pady=5)

        ttk.Label(frame_login, text="Contraseña:").grid(row=2, column=0, pady=5)
        self.contrasena = ttk.Entry(frame_login, show="*")
        self.contrasena.grid(row=2, column=1, pady=5)

        # Botones
        ttk.Button(frame_login, text="Iniciar Sesión", 
                  command=self.iniciar_sesion).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Separador
        ttk.Separator(frame_login, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)
        
        # Texto y botón de registro
        ttk.Label(frame_login, text="¿No tienes una cuenta?").grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(frame_login, text="Registrarse como Estudiante", 
                  command=self.mostrar_registro).grid(row=6, column=0, columnspan=2, pady=5)

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

        # Botón para ver participantes
        ttk.Button(frame_lista, text="Ver Participantes", 
                  command=self.mostrar_participantes_evento).grid(row=3, column=0, pady=5)

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

        # Lista de usuarios existentes
        frame_lista = ttk.LabelFrame(frame_usuarios, text="Usuarios Existentes", padding="10")
        frame_lista.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        # TreeView para mostrar usuarios
        self.tree_usuarios = ttk.Treeview(frame_lista, 
                                        columns=('ID', 'Nombre', 'Correo', 'Rol'),
                                        show='headings')
        self.tree_usuarios.heading('ID', text='ID')
        self.tree_usuarios.heading('Nombre', text='Nombre')
        self.tree_usuarios.heading('Correo', text='Correo')
        self.tree_usuarios.heading('Rol', text='Rol')
        
        # Configurar anchos de columna
        self.tree_usuarios.column('ID', width=50)
        self.tree_usuarios.column('Nombre', width=200)
        self.tree_usuarios.column('Correo', width=200)
        self.tree_usuarios.column('Rol', width=100)
        
        self.tree_usuarios.grid(row=0, column=0, pady=5)

        # Frame para botones
        frame_botones = ttk.Frame(frame_lista)
        frame_botones.grid(row=1, column=0, pady=5)

        # Botones de acción
        ttk.Button(frame_botones, text="Cambiar Rol", 
                  command=self.cambiar_rol_usuario).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botones, text="Eliminar Usuario", 
                  command=self.eliminar_usuario).grid(row=0, column=1, padx=5)

        # Botón para volver
        ttk.Button(frame_usuarios, text="Volver", 
                  command=self.mostrar_pantalla_principal).grid(row=2, column=0, pady=20)

        # Cargar lista de usuarios
        self.cargar_lista_usuarios()

    def cambiar_rol_usuario(self):
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return

        usuario_id = self.tree_usuarios.item(seleccion[0])['values'][0]
        rol_actual = self.tree_usuarios.item(seleccion[0])['values'][3]
        nombre_usuario = self.tree_usuarios.item(seleccion[0])['values'][1]

        # Crear ventana emergente para cambiar rol
        ventana_rol = tk.Toplevel(self.ventana)
        ventana_rol.title("Cambiar Rol de Usuario")
        ventana_rol.geometry("300x200")

        # Frame principal
        frame_rol = ttk.Frame(ventana_rol, padding="20")
        frame_rol.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Etiqueta informativa
        ttk.Label(frame_rol, 
                 text=f"Usuario: {nombre_usuario}\nRol actual: {rol_actual}",
                 justify="center").grid(row=0, column=0, columnspan=2, pady=10)

        # Combobox para seleccionar nuevo rol
        ttk.Label(frame_rol, text="Nuevo rol:").grid(row=1, column=0, pady=5)
        nuevo_rol = ttk.Combobox(frame_rol, values=['estudiante', 'administrador'])
        nuevo_rol.set(rol_actual)
        nuevo_rol.grid(row=1, column=1, pady=5)

        def guardar_cambio_rol():
            try:
                cursor = self.db.conexion.cursor()
                cursor.execute("""
                    UPDATE usuarios 
                    SET rol = %s 
                    WHERE id = %s
                """, (nuevo_rol.get(), usuario_id))
                self.db.conexion.commit()
                messagebox.showinfo("Éxito", "Rol actualizado exitosamente")
                ventana_rol.destroy()
                self.cargar_lista_usuarios()  # Actualizar lista de usuarios
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar rol: {e}")
            finally:
                cursor.close()

        # Botones
        ttk.Button(frame_rol, text="Guardar", 
                  command=guardar_cambio_rol).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(frame_rol, text="Cancelar", 
                  command=ventana_rol.destroy).grid(row=3, column=0, columnspan=2, pady=5)

    def cargar_lista_usuarios(self):
        # Limpiar lista actual
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        try:
            cursor = self.db.conexion.cursor()
            cursor.execute("SELECT id, nombre, correo, rol FROM usuarios ORDER BY nombre")
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
                self.cargar_lista_usuarios()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar usuario: {e}")
            finally:
                cursor.close()

    def mostrar_eventos_disponibles(self):
        # Limpiar ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()

        # Frame principal
        frame_eventos = ttk.Frame(self.ventana, padding="20")
        frame_eventos.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        ttk.Label(frame_eventos, text="Eventos Disponibles", 
                 font=('Helvetica', 14, 'bold')).grid(row=0, column=0, pady=10)

        # TreeView para mostrar eventos
        self.tree_eventos = ttk.Treeview(frame_eventos, 
                                       columns=('ID', 'Título', 'Fecha', 'Hora', 'Lugar', 'Categoría', 'Estado'),
                                       show='headings')
        self.tree_eventos.heading('ID', text='ID')
        self.tree_eventos.heading('Título', text='Título')
        self.tree_eventos.heading('Fecha', text='Fecha')
        self.tree_eventos.heading('Hora', text='Hora')
        self.tree_eventos.heading('Lugar', text='Lugar')
        self.tree_eventos.heading('Categoría', text='Categoría')
        self.tree_eventos.heading('Estado', text='Estado')
        
        # Configurar el ancho de las columnas
        self.tree_eventos.column('ID', width=50)
        self.tree_eventos.column('Título', width=200)
        self.tree_eventos.column('Fecha', width=100)
        self.tree_eventos.column('Hora', width=80)
        self.tree_eventos.column('Lugar', width=150)
        self.tree_eventos.column('Categoría', width=100)
        self.tree_eventos.column('Estado', width=100)
        
        self.tree_eventos.grid(row=1, column=0, pady=5)

        # Frame para detalles del evento
        frame_detalles = ttk.LabelFrame(frame_eventos, text="Detalles del Evento", padding="10")
        frame_detalles.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))

        # Etiquetas para mostrar detalles
        self.detalle_titulo = ttk.Label(frame_detalles, text="")
        self.detalle_titulo.grid(row=0, column=0, pady=5)
        self.detalle_descripcion = ttk.Label(frame_detalles, text="")
        self.detalle_descripcion.grid(row=1, column=0, pady=5)

        # Botón para inscribirse
        self.boton_inscribir = ttk.Button(frame_detalles, text="Inscribirse al Evento", 
                                        command=self.inscribir_evento)
        self.boton_inscribir.grid(row=2, column=0, pady=10)

        # Botón para volver
        ttk.Button(frame_eventos, text="Volver", 
                  command=self.mostrar_pantalla_principal).grid(row=3, column=0, pady=20)

        # Vincular evento de selección
        self.tree_eventos.bind('<<TreeviewSelect>>', self.mostrar_detalles_evento)

        # Cargar eventos disponibles
        self.cargar_eventos_disponibles()

    def cargar_eventos_disponibles(self):
        # Limpiar lista actual
        for item in self.tree_eventos.get_children():
            self.tree_eventos.delete(item)
        
        try:
            cursor = self.db.conexion.cursor()
            # Agregamos una columna calculada para el estado del evento
            cursor.execute("""
                SELECT 
                    e.id, 
                    e.titulo, 
                    DATE_FORMAT(e.fecha, '%Y-%m-%d') as fecha, 
                    TIME_FORMAT(e.hora, '%H:%i') as hora, 
                    e.lugar, 
                    e.categoria,
                    CASE 
                        WHEN e.fecha < CURDATE() THEN 'Caducado'
                        WHEN e.fecha = CURDATE() THEN 'Hoy'
                        WHEN e.fecha <= DATE_ADD(CURDATE(), INTERVAL 7 DAY) THEN 'Próximo'
                        ELSE 'Futuro'
                    END as estado
                FROM eventos e 
                ORDER BY e.fecha, e.hora
            """)
            
            # Actualizar la estructura del TreeView para incluir la columna de estado
            self.tree_eventos['columns'] = ('ID', 'Título', 'Fecha', 'Hora', 'Lugar', 'Categoría', 'Estado')
            self.tree_eventos.heading('ID', text='ID')
            self.tree_eventos.heading('Título', text='Título')
            self.tree_eventos.heading('Fecha', text='Fecha')
            self.tree_eventos.heading('Hora', text='Hora')
            self.tree_eventos.heading('Lugar', text='Lugar')
            self.tree_eventos.heading('Categoría', text='Categoría')
            self.tree_eventos.heading('Estado', text='Estado')
            
            # Configurar el ancho de las columnas
            self.tree_eventos.column('ID', width=50)
            self.tree_eventos.column('Título', width=200)
            self.tree_eventos.column('Fecha', width=100)
            self.tree_eventos.column('Hora', width=80)
            self.tree_eventos.column('Lugar', width=150)
            self.tree_eventos.column('Categoría', width=100)
            self.tree_eventos.column('Estado', width=100)
            
            eventos = cursor.fetchall()
            if not eventos:
                self.detalle_titulo.config(text="No hay eventos disponibles")
                self.detalle_descripcion.config(text="")
                self.boton_inscribir.state(['disabled'])
            else:
                for evento in eventos:
                    # Configurar color según el estado
                    estado = evento[6]  # El estado es el último elemento
                    if estado == 'Caducado':
                        tag = 'caducado'
                    elif estado == 'Hoy':
                        tag = 'hoy'
                    elif estado == 'Próximo':
                        tag = 'proximo'
                    else:
                        tag = 'futuro'
                    
                    self.tree_eventos.insert('', 'end', values=evento, tags=(tag,))
                
                # Configurar colores para los diferentes estados
                self.tree_eventos.tag_configure('caducado', foreground='gray')
                self.tree_eventos.tag_configure('hoy', foreground='green')
                self.tree_eventos.tag_configure('proximo', foreground='blue')
                self.tree_eventos.tag_configure('futuro', foreground='black')
                
                self.boton_inscribir.state(['!disabled'])
                
            # Imprimir para debug
            print("Eventos cargados:", eventos)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar eventos: {e}")
            print(f"Error detallado: {e}")
        finally:
            cursor.close()

    def mostrar_detalles_evento(self, event):
        seleccion = self.tree_eventos.selection()
        if seleccion:
            evento_id = self.tree_eventos.item(seleccion[0])['values'][0]
            estado = self.tree_eventos.item(seleccion[0])['values'][6]  # Obtener el estado del evento
            
            try:
                cursor = self.db.conexion.cursor()
                cursor.execute("""
                    SELECT e.titulo, e.descripcion, e.fecha, e.hora, e.lugar, e.categoria
                    FROM eventos e
                    WHERE e.id = %s
                """, (evento_id,))
                evento = cursor.fetchone()
                if evento:
                    # Mostrar detalles más completos
                    detalles = f"""
                    Título: {evento[0]}
                    Fecha: {evento[2]}
                    Hora: {evento[3]}
                    Lugar: {evento[4]}
                    Categoría: {evento[5]}
                    """
                    self.detalle_titulo.config(text=detalles)
                    self.detalle_descripcion.config(text=f"Descripción: {evento[1]}")
                    
                    # Si el evento está caducado, deshabilitar el botón de inscripción
                    if estado == 'Caducado':
                        self.boton_inscribir.state(['disabled'])
                        self.boton_inscribir.config(text="Evento Caducado")
                    else:
                        self.boton_inscribir.state(['!disabled'])
                        # Verificar si el usuario ya está inscrito
                        cursor.execute("""
                            SELECT * FROM inscripciones 
                            WHERE evento_id = %s AND estudiante_id = %s
                        """, (evento_id, self.usuario_actual['id']))
                        
                        if cursor.fetchone():
                            self.boton_inscribir.config(text="Cancelar Inscripción")
                        else:
                            self.boton_inscribir.config(text="Inscribirse al Evento")
                            
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar detalles: {e}")
                print(f"Error detallado: {e}")
            finally:
                cursor.close()

    def inscribir_evento(self):
        seleccion = self.tree_eventos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un evento")
            return

        evento_id = self.tree_eventos.item(seleccion[0])['values'][0]
        estado = self.tree_eventos.item(seleccion[0])['values'][6]  # Obtener el estado del evento
        
        # Verificar si el evento está caducado
        if estado == 'Caducado':
            messagebox.showwarning("Advertencia", "No es posible inscribirse a eventos caducados")
            return
        
        try:
            cursor = self.db.conexion.cursor()
            # Verificar si ya está inscrito
            cursor.execute("""
                SELECT * FROM inscripciones 
                WHERE evento_id = %s AND estudiante_id = %s
            """, (evento_id, self.usuario_actual['id']))
            
            inscripcion = cursor.fetchone()
            
            if inscripcion:
                # Cancelar inscripción
                cursor.execute("""
                    DELETE FROM inscripciones 
                    WHERE evento_id = %s AND estudiante_id = %s
                """, (evento_id, self.usuario_actual['id']))
                messagebox.showinfo("Éxito", "Inscripción cancelada exitosamente")
                self.boton_inscribir.config(text="Inscribirse al Evento")
            else:
                # Realizar inscripción
                cursor.execute("""
                    INSERT INTO inscripciones (evento_id, estudiante_id)
                    VALUES (%s, %s)
                """, (evento_id, self.usuario_actual['id']))
                messagebox.showinfo("Éxito", "Inscripción realizada exitosamente")
                self.boton_inscribir.config(text="Cancelar Inscripción")
            
            self.db.conexion.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error en la inscripción: {e}")
        finally:
            cursor.close()

    def mostrar_mis_inscripciones(self):
        # Limpiar ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()

        # Frame principal
        frame_inscripciones = ttk.Frame(self.ventana, padding="20")
        frame_inscripciones.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        ttk.Label(frame_inscripciones, text="Mis Inscripciones", 
                 font=('Helvetica', 14, 'bold')).grid(row=0, column=0, pady=10)

        # TreeView para mostrar inscripciones
        self.tree_inscripciones = ttk.Treeview(frame_inscripciones, 
                                             columns=('ID', 'Evento', 'Fecha', 'Hora', 'Lugar'),
                                             show='headings')
        self.tree_inscripciones.heading('ID', text='ID')
        self.tree_inscripciones.heading('Evento', text='Evento')
        self.tree_inscripciones.heading('Fecha', text='Fecha')
        self.tree_inscripciones.heading('Hora', text='Hora')
        self.tree_inscripciones.heading('Lugar', text='Lugar')
        self.tree_inscripciones.grid(row=1, column=0, pady=5)

        # Botón para cancelar inscripción
        ttk.Button(frame_inscripciones, text="Cancelar Inscripción Seleccionada", 
                  command=self.cancelar_inscripcion).grid(row=2, column=0, pady=10)

        # Botón para volver
        ttk.Button(frame_inscripciones, text="Volver", 
                  command=self.mostrar_pantalla_principal).grid(row=3, column=0, pady=20)

        # Cargar inscripciones
        self.cargar_mis_inscripciones()

    def cargar_mis_inscripciones(self):
        # Limpiar lista actual
        for item in self.tree_inscripciones.get_children():
            self.tree_inscripciones.delete(item)
        
        try:
            cursor = self.db.conexion.cursor()
            cursor.execute("""
                SELECT i.id, e.titulo, e.fecha, e.hora, e.lugar
                FROM inscripciones i
                JOIN eventos e ON i.evento_id = e.id
                WHERE i.estudiante_id = %s
                ORDER BY e.fecha, e.hora
            """, (self.usuario_actual['id'],))
            
            for inscripcion in cursor.fetchall():
                self.tree_inscripciones.insert('', 'end', values=inscripcion)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar inscripciones: {e}")
        finally:
            cursor.close()

    def cancelar_inscripcion(self):
        seleccion = self.tree_inscripciones.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione una inscripción para cancelar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar esta inscripción?"):
            try:
                inscripcion_id = self.tree_inscripciones.item(seleccion[0])['values'][0]
                cursor = self.db.conexion.cursor()
                cursor.execute("DELETE FROM inscripciones WHERE id = %s", (inscripcion_id,))
                self.db.conexion.commit()
                messagebox.showinfo("Éxito", "Inscripción cancelada exitosamente")
                self.cargar_mis_inscripciones()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cancelar inscripción: {e}")
            finally:
                cursor.close()

    def mostrar_participantes_evento(self):
        # Verificar si hay un evento seleccionado
        seleccion = self.tree_eventos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un evento")
            return

        evento_id = self.tree_eventos.item(seleccion[0])['values'][0]
        evento_titulo = self.tree_eventos.item(seleccion[0])['values'][1]

        # Crear ventana emergente
        ventana_participantes = tk.Toplevel(self.ventana)
        ventana_participantes.title(f"Participantes - {evento_titulo}")
        ventana_participantes.geometry("600x400")

        # Frame principal
        frame_participantes = ttk.Frame(ventana_participantes, padding="20")
        frame_participantes.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        ttk.Label(frame_participantes, 
                 text=f"Lista de Participantes - {evento_titulo}", 
                 font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=10)

        # TreeView para mostrar participantes
        tree_participantes = ttk.Treeview(frame_participantes, 
                                        columns=('ID', 'Nombre', 'Correo', 'Fecha Inscripción'),
                                        show='headings')
        tree_participantes.heading('ID', text='ID')
        tree_participantes.heading('Nombre', text='Nombre')
        tree_participantes.heading('Correo', text='Correo')
        tree_participantes.heading('Fecha Inscripción', text='Fecha Inscripción')
        tree_participantes.grid(row=1, column=0, pady=5)

        # Cargar participantes
        try:
            cursor = self.db.conexion.cursor()
            cursor.execute("""
                SELECT u.id, u.nombre, u.correo, i.fecha_inscripcion
                FROM usuarios u
                JOIN inscripciones i ON u.id = i.estudiante_id
                WHERE i.evento_id = %s
                ORDER BY i.fecha_inscripcion
            """, (evento_id,))
            
            for participante in cursor.fetchall():
                tree_participantes.insert('', 'end', values=participante)

            # Mostrar total de participantes
            total = tree_participantes.get_children()
            ttk.Label(frame_participantes, 
                     text=f"Total de participantes: {len(total)}", 
                     font=('Helvetica', 10)).grid(row=2, column=0, pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar participantes: {e}")
        finally:
            cursor.close()

    def mostrar_registro(self):
        # Limpiar ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()

        # Frame de registro
        frame_registro = ttk.Frame(self.ventana, padding="20")
        frame_registro.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        ttk.Label(frame_registro, text="Registro de Estudiante", 
                 font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos de registro
        ttk.Label(frame_registro, text="Nombre completo:").grid(row=1, column=0, pady=5)
        self.registro_nombre = ttk.Entry(frame_registro)
        self.registro_nombre.grid(row=1, column=1, pady=5)

        ttk.Label(frame_registro, text="Correo electrónico:").grid(row=2, column=0, pady=5)
        self.registro_correo = ttk.Entry(frame_registro)
        self.registro_correo.grid(row=2, column=1, pady=5)

        ttk.Label(frame_registro, text="Contraseña:").grid(row=3, column=0, pady=5)
        self.registro_contrasena = ttk.Entry(frame_registro, show="*")
        self.registro_contrasena.grid(row=3, column=1, pady=5)

        ttk.Label(frame_registro, text="Confirmar contraseña:").grid(row=4, column=0, pady=5)
        self.registro_confirmar = ttk.Entry(frame_registro, show="*")
        self.registro_confirmar.grid(row=4, column=1, pady=5)

        # Botones
        ttk.Button(frame_registro, text="Registrarse", 
                  command=self.registrar_estudiante).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(frame_registro, text="Volver", 
                  command=self.mostrar_login).grid(row=6, column=0, columnspan=2, pady=5)

    def registrar_estudiante(self):
        # Obtener datos del formulario
        nombre = self.registro_nombre.get()
        correo = self.registro_correo.get()
        contrasena = self.registro_contrasena.get()
        confirmar = self.registro_confirmar.get()

        # Validaciones básicas
        if not all([nombre, correo, contrasena, confirmar]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if contrasena != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        if not '@' in correo:
            messagebox.showerror("Error", "Correo electrónico inválido")
            return

        try:
            cursor = self.db.conexion.cursor()
            
            # Verificar si el correo ya existe
            cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Este correo ya está registrado")
                return

            # Insertar nuevo estudiante
            query = """
                INSERT INTO usuarios (nombre, correo, contrasena, rol)
                VALUES (%s, %s, %s, 'estudiante')
            """
            cursor.execute(query, (nombre, correo, contrasena))
            self.db.conexion.commit()
            
            messagebox.showinfo("Éxito", "Registro exitoso. Ya puedes iniciar sesión.")
            self.mostrar_login()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {e}")
        finally:
            cursor.close()

if __name__ == "__main__":
    app = SistemaEventos()
    app.ejecutar()
