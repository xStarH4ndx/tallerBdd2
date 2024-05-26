import psycopg2

def crear_conexion():
    # Conectar a la base de datos
    conexion = psycopg2.connect(
        database="taller2_bdd",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    return conexion

def registrar_usuario(conexion, nombre, email, password, tipo):
    try:
        with conexion.cursor() as cur:
            cur.execute("INSERT INTO usuario (nombre, email, password, tipo) VALUES (%s, %s, %s, %s)", (nombre, email, password, tipo))
            conexion.commit()
            print("\n---Usuario registrado con éxito---")
    except psycopg2.errors.UniqueViolation:
        conexion.rollback()
        print("\n---El email ya existe---")

def login_usuario(conexion, email, password):
    with conexion.cursor() as cur:
        cur.execute("SELECT password, tipo FROM usuario WHERE email = %s", (email,))
        result = cur.fetchone()
        if result and result[0] == password:
            print("\n---Inicio de sesión exitoso---")
            return result[1]  # Devolver el tipo de usuario
        else:
            print("---Email o contraseña incorrectos---")
            return None


'''-------------------------OPCIONES USUARIO----------------------------'''

def ver_informacion_personal(conexion, email):
    with conexion.cursor() as cur:
        cur.execute("SELECT nombre, email FROM usuario WHERE email = %s", (email,))
        usuario = cur.fetchone()
        if usuario:
            print("\n---Información Personal---")
            print(f"Nombre: {usuario[0]}")
            print(f"Email: {usuario[1]}")
        else:
            print("\n---Usuario no encontrado---")

def listar_productos(conexion):
    with conexion.cursor() as cur:
        cur.execute("SELECT id_producto, nombre, descripcion, precio, cant_stock FROM producto ORDER BY id_producto")
        productos = cur.fetchall()
        print("\n---Catálogo de Productos---")
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Precio: {producto[3]}, Stock: {producto[4]}")

def realizar_compra(conexion, email_user):
    with conexion.cursor() as cur:
        listar_productos(conexion)
        producto_id = int(input("\nIngrese el ID del producto que desea comprar: "))
        cantidad = int(input("Ingrese la cantidad: "))

        # Obtener el precio del producto y verificar stock
        cur.execute("SELECT precio, cant_stock FROM producto WHERE id_producto = %s", (producto_id,))
        producto = cur.fetchone()
        
        if (producto) and (producto[1] >= cantidad): # Si el producto es != None y el stock del producto es mayor o igual a la cantidad de compra
            precio_total = producto[0] * cantidad
            nuevo_stock = producto[1] - cantidad

            # Insertar en la tabla venta
            cur.execute("INSERT INTO venta (email, id_producto, monto_total) VALUES (%s, %s, %s)", (email_user, producto_id, precio_total))
            
            # Actualizar el stock del producto
            cur.execute("UPDATE producto SET cant_stock = %s WHERE id_producto = %s", (nuevo_stock, producto_id))
            
            conexion.commit()
            print("\n---Compra realizada con éxito---")
        else:
            conexion.rollback()
            print("\n---Stock insuficiente o producto no encontrado---")


'''-------------------------OPCIONES ADMINISTRADOR----------------------------'''

#El administrador puede ingresar los detalles de un nuevo 
#producto, como nombre, descripción, precio y cantidad en stock.
def registrar_producto(conexion):
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción del producto: ")
    precio = int(input("Precio del producto: "))
    cant_stock = int(input("Cantidad en stock: "))

    with conexion.cursor() as cur:
        cur.execute("INSERT INTO producto (nombre, descripcion, precio, cant_stock) VALUES (%s, %s, %s, %s)", (nombre, descripcion, precio, cant_stock))
        conexion.commit()
        print("\n---Producto registrado con éxito---")

#El administrador puede buscar y ver los detalles de un 
#producto en particular, incluyendo su información y cantidad en stock
def ver_detalles_producto(conexion):
    mostrar_inventario(conexion)
    producto_id = int(input("\nIngrese el ID del producto: "))

    with conexion.cursor() as cur:
        cur.execute("SELECT id_producto, nombre, descripcion, precio, cant_stock FROM producto WHERE id_producto = %s", (producto_id,))
        producto = cur.fetchone()
        if producto:
            print("\n---Información del Producto---")
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Precio: {producto[3]}, Stock: {producto[4]}")
        else:
            print("\n---Producto no encontrado---")

def mostrar_inventario(conexion):
    with conexion.cursor() as cur:
        cur.execute("SELECT id_producto, nombre FROM producto ORDER BY id_producto")
        productos = cur.fetchall()
        if productos:
            print("\n---Inventario---")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}")
        else:
            print("\n---No hay productos en el inventario---")


#El administrador puede seleccionar un producto y actualizar su
#cantidad en stock o precio.
def actualizar_inventario(conexion):
    mostrar_inventario(conexion)
    producto_id = int(input("\nIngrese el ID del producto: "))
    nuevo_precio = int(input("Nuevo precio del producto: "))
    nueva_cant_stock = int(input("Nueva cantidad en stock: "))

    with conexion.cursor() as cur:
        cur.execute("UPDATE producto SET precio = %s, cant_stock = %s WHERE id_producto = %s", (nuevo_precio, nueva_cant_stock, producto_id))
        conexion.commit()
        print("\n---Inventario actualizado con éxito---")

#El sistema muestra una lista de los productos 
#que tienen una cantidad en stock por debajo de un umbral definido*, junto con su información
def ver_productos_bajo_stock(conexion, cantidad_minima=10):
    with conexion.cursor() as cur:
        cur.execute("SELECT id_producto, nombre, descripcion, precio, cant_stock FROM producto WHERE cant_stock < %s ORDER BY id_producto", (cantidad_minima,))
        productos = cur.fetchall()
        print("\n---Productos Bajos en Stock---")
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Precio: {producto[3]}, Stock: {producto[4]}")

#El administrador puede registrar una venta, indicando los productos 
#vendidos y la cantidad de cada uno
def registrar_venta(conexion):
    email_user = input("Email del usuario: ")
    listar_productos(conexion)
    producto_id = int(input("\nIngrese el ID del producto que desea vender: "))
    cantidad = int(input("Ingrese la cantidad: "))

    with conexion.cursor() as cur:
        cur.execute("SELECT precio, cant_stock FROM producto WHERE id_producto = %s", (producto_id,))
        producto = cur.fetchone()
        
        if (producto) and (producto[1] >= cantidad):
            precio_total = producto[0] * cantidad
            nuevo_stock = producto[1] - cantidad

            cur.execute("INSERT INTO venta (email, id_producto, monto_total) VALUES (%s, %s, %s)", (email_user, producto_id, precio_total))
            cur.execute("UPDATE producto SET cant_stock = %s WHERE id_producto = %s", (nuevo_stock, producto_id))
            
            conexion.commit()
            print("\n---Venta registrada con éxito---")
        else:
            conexion.rollback()
            print("\n---Stock insuficiente o producto no encontrado---")
            
#El sistema muestra un registro de las ventas realizadas, 
#incluyendo los productos vendidos y el monto total
def ver_historial_ventas(conexion):
    with conexion.cursor() as cur:
        cur.execute("SELECT id_venta, email, id_producto, monto_total FROM venta")
        ventas = cur.fetchall()
        print("\n---Historial de Ventas---")
        for venta in ventas:
            print(f"ID Venta: {venta[0]}, Email: {venta[1]}, ID Producto: {venta[2]}, Monto Total: {venta[3]}")


'''--------------------------DESPLEGAR MENUS DE OPCIONES-----------------------'''
def menu_usuario(conexion, email):
    while True:
        print("\n------MENU DE USUARIO------")
        print("1) Ver información personal")
        print("2) Ver catálogo de productos")
        print("3) Realizar una compra")
        print("4) Salir")
        opcion_usuario = input("\nElige una opción: ")

        if opcion_usuario == '1':
            ver_informacion_personal(conexion, email)
        elif opcion_usuario == '2':
            listar_productos(conexion)
        elif opcion_usuario == '3':
            realizar_compra(conexion, email)
        elif opcion_usuario == '4':
            print("\n---Saliendo del sistema---")
            break
        else:
            print("Opción no válida.")

def menu_admin(conexion, email):
    while True:
        print("\n------MENU DE ADMINISTRADOR------")
        print("1) Registrar nuevo producto")
        print("2) Ver información de un producto")
        print("3) Actualizar inventario")
        print("4) Ver informes de productos bajos en stock")
        print("5) Registrar una venta")
        print("6) Ver historial de ventas")
        print("7) Salir")
        opcion_admin = input("\nElige una opción: ")

        if opcion_admin == '1':
            registrar_producto(conexion)
        elif opcion_admin == '2':
            ver_detalles_producto(conexion)
        elif opcion_admin == '3':
            actualizar_inventario(conexion)
        elif opcion_admin == '4':
            ver_productos_bajo_stock(conexion)
        elif opcion_admin == '5':
            registrar_venta(conexion)
        elif opcion_admin == '6':
            ver_historial_ventas(conexion)
        elif opcion_admin == '7':
            print("\n---Saliendo del sistema---")
            break
        else:
            print("Opción no válida.")

'''---------------INICIO DEL PROGRAMA--------------'''
def main():
    conexion = crear_conexion()

    while True:
        print("------BIENVENIDO------")
        print("1) Registrarse")
        print("2) Iniciar sesión")
        print("3) Salir")
        opcion = input("\nElige una opción: ")

        if opcion == '1':
            print("------------------")
            print("     REGISTRO     ")
            print("------------------")
            nombre = input("Nombre: ")
            email = input("Email: ")
            password = input("Contraseña: ")
            registrar_usuario(conexion, nombre, email, password, 'usuario') # todos los usuarios registrados serán usuarios normales
        
        elif opcion == '2':
            print("------------------")
            print("  INICIAR SESION  ")
            print("------------------")
            email = input("Email: ")
            password = input("Contraseña: ")
            tipo_usuario = login_usuario(conexion, email, password)
            
            if tipo_usuario == 'usuario':
                menu_usuario(conexion, email)
            elif tipo_usuario == 'admin':
                menu_admin(conexion, email)
                
        elif opcion == '3':
            print("------------------")
            print("     SALIENDO     ")
            print("------------------")
            break
        else:
            print("Opción no válida.")

    conexion.close()

if __name__ == "__main__":
    main()
