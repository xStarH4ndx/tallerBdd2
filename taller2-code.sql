/*
--------TALLER 2 BDD-----------
Nombres:
	- Nicolas
	- Bruno Toro - 20864066-6
*/

create table usuario(
	id_usuario integer primary key,
	email text not null,
	password text not null,
	tipo text not null
);

create table producto(
	id_producto integer primary key,
	nombre text not null,
	descripcion text not null,
	precio integer not null,
	cant_stock integer not null
);

create table venta(
	id_venta integer primary key,
	id_usuario integer references usuario(id_usuario),
	id_producto integer references producto(id_producto),
	monto_total integer not null
);
