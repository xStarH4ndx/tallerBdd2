/*
--------TALLER 2 BDD-----------
Nombres:
	- Nicolas Aburto Lopez - 18758339-K - ICCI
	- Bruno Toro - 20864066-6 - ICCI

DROP TABLE IF EXISTS venta;
DROP TABLE IF EXISTS producto;
DROP TABLE IF EXISTS usuario;
*/

create table usuario(
	nombre text not null,
	email text primary key,
	password text not null,
	tipo text not null
);

create table producto(
	id_producto serial primary key,
	nombre text not null,
	descripcion text not null,
	precio integer not null,
	cant_stock integer not null
);

--serial significa que aumentará en 1 cada vez que se ingrese una venta
create table venta(
	id_venta serial primary key,
	email text references usuario(email),
	id_producto integer references producto(id_producto),
	monto_total integer not null
);

--Poblar Usuario
insert into usuario (nombre,email,password,tipo) values
('Camilo Cerda','camilo@tienda.com','camilo@7720','admin')

--Poblar Productos
insert into producto (nombre, descripcion, precio, cant_stock) values
('Laptop','Laptop con 8GB RAM', 1200, 50),
('Celular','Celular con 128GB',800,100),
('Tablet','Tablet con 64GB', 300, 75),
('Audifonos','Audifonos inalámbricos', 150, 200),
('Monitor','Monitor de 27 pulgadas', 350, 30),
('Teclado','Teclado mecánico', 100, 150),
('Mouse','Mouse inalámbrico', 50, 200),
('Impresora','Impresora con conexión Wi-Fi', 200, 40),
('Cámara','Cámara digital con lente de 24MP', 600, 20),
('Parlante Bluetooth','Parlante aprueba de agua', 80, 300);


insert into usuario (nombre,email,password,tipo) values
('bruno','a@a','a123','usuario')