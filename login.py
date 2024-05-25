import psycopg2

def create_connection():
    # Conectar a la base de datos
    conexion = psycopg2.connect(
        database="taller_2_bdd",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    return conexion

def register_user(conexion, email, password, tipo):
    try:
        with conexion.cursor() as cur:
            cur.execute("INSERT INTO usuario (email, password, tipo) VALUES (%s, %s, %s)", (email, password, tipo))
            conexion.commit()
            print("\n---Usuario registrado con éxito---")
    except psycopg2.errors.UniqueViolation:
        conexion.rollback()
        print("\n---El email ya existe---")

def login_user(conexion, email, password):
    with conexion.cursor() as cur:
        cur.execute("SELECT password FROM usuario WHERE email = %s", (email,))
        result = cur.fetchone()
        if result and result[0] == password: #Si el resultado != none, y la contraseña es valida, inicia sesion
            print("\n---Inicio de sesión exitoso---")
        else:
            print("---Email o contraseña incorrectos---")

def main():
    conexion = create_connection()

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
            email = input("Email: ")
            password = input("Contraseña: ")
            register_user(conexion, email, password, 'usuario')
        elif opcion == '2':
            print("------------------")
            print("  INICIAR SESION  ")
            print("------------------")
            email = input("Email: ")
            password = input("Contraseña: ")
            login_user(conexion, email, password)
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
