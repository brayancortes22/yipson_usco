from base_de_datos import BaseDatos

def inicializar_sistema():
    # Crear instancia de la base de datos
    db = BaseDatos()
    
    # Crear las tablas necesarias
    db.crear_tablas()
    
    # Crear usuario administrador por defecto
    crear_admin_default(db)

def crear_admin_default(db):
    try:
        cursor = db.conexion.cursor()
        # Verificar si ya existe un administrador
        cursor.execute("SELECT * FROM usuarios WHERE rol = 'administrador' LIMIT 1")
        if not cursor.fetchone():
            # Crear administrador por defecto
            query = """
                INSERT INTO usuarios (nombre, correo, contrasena, rol)
                VALUES (%s, %s, %s, %s)
            """
            valores = ('Admin', 'admin@usco.edu.co', 'admin123', 'administrador')
            cursor.execute(query, valores)
            db.conexion.commit()
            print("Administrador por defecto creado exitosamente")
    except Exception as e:
        print(f"Error al crear administrador por defecto: {e}")

if __name__ == "__main__":
    inicializar_sistema()
