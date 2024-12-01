import mysql.connector
from mysql.connector import Error

class BaseDatos:
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host='localhost',
                user='root',  # Usuario por defecto en XAMPP
                password='',  # Contraseña por defecto en XAMPP
                port=3306    # Puerto por defecto
            )
            
            # Crear la base de datos si no existe
            cursor = self.conexion.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS eventos_universitarios")
            cursor.execute("USE eventos_universitarios")
            
            if self.conexion.is_connected():
                print("Conexión exitosa a la base de datos")
                self.crear_tablas()
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def crear_tablas(self):
        try:
            cursor = self.conexion.cursor()
            
            # Tabla Usuarios con motor InnoDB para soporte de claves foráneas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    correo VARCHAR(100) UNIQUE NOT NULL,
                    contrasena VARCHAR(255) NOT NULL,
                    rol ENUM('administrador', 'estudiante') NOT NULL
                ) ENGINE=InnoDB;
            ''')

            # Tabla Eventos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS eventos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    titulo VARCHAR(200) NOT NULL,
                    descripcion TEXT,
                    fecha DATE NOT NULL,
                    hora TIME NOT NULL,
                    lugar VARCHAR(200) NOT NULL,
                    categoria VARCHAR(100) NOT NULL,
                    administrador_id INT,
                    FOREIGN KEY (administrador_id) REFERENCES usuarios(id)
                    ON DELETE SET NULL
                ) ENGINE=InnoDB;
            ''')

            # Tabla Inscripciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inscripciones (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    evento_id INT,
                    estudiante_id INT,
                    fecha_inscripcion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (evento_id) REFERENCES eventos(id)
                    ON DELETE CASCADE,
                    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id)
                    ON DELETE CASCADE
                ) ENGINE=InnoDB;
            ''')

            self.conexion.commit()
            print("Tablas creadas exitosamente")
            
        except Error as e:
            print(f"Error al crear las tablas: {e}")
            
    def cerrar_conexion(self):
        if hasattr(self, 'conexion') and self.conexion.is_connected():
            self.conexion.close()
            print("Conexión a la base de datos cerrada")
