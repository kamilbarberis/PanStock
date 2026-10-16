CREATE DATABASE IF NOT EXISTS panstock
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE panstock;

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(150),
    CONSTRAINT chk_categoria_nombre CHECK (CHAR_LENGTH(TRIM(nombre)) > 0)
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(200),
    precio DECIMAL(10,2) NOT NULL,
    stock_minimo INT NOT NULL DEFAULT 5,
    id_categoria INT NOT NULL,
    CONSTRAINT chk_producto_nombre CHECK (CHAR_LENGTH(TRIM(nombre)) > 0),
    CONSTRAINT chk_producto_precio CHECK (precio >= 0),
    CONSTRAINT chk_producto_stock_minimo CHECK (stock_minimo >= 0),
    CONSTRAINT fk_productos_categorias
        FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS movimientos (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    tipo_movimiento VARCHAR(10) NOT NULL,
    cantidad INT NOT NULL,
    fecha DATETIME NOT NULL,
    observacion VARCHAR(200),
    CONSTRAINT chk_movimiento_tipo
        CHECK (tipo_movimiento IN ('ENTRADA', 'SALIDA')),
    CONSTRAINT chk_movimiento_cantidad CHECK (cantidad > 0),
    CONSTRAINT fk_movimientos_productos
        FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

INSERT IGNORE INTO categorias (nombre, descripcion) VALUES
('Panadería', 'Variedades de panes tradicionales y artesanales'),
('Facturería', 'Facturas, criollos, medialunas y hojaldres'),
('Repostería', 'Tortas, tartas dulces, postres y masitas');

INSERT INTO productos (nombre, descripcion, precio, stock_minimo, id_categoria)
SELECT 'Pan Francés (Kg)', 'Pan tradicional tipo francés', 2200.00, 10, c.id_categoria
FROM categorias c WHERE c.nombre = 'Panadería'
AND NOT EXISTS (SELECT 1 FROM productos p WHERE p.nombre = 'Pan Francés (Kg)');

INSERT INTO productos (nombre, descripcion, precio, stock_minimo, id_categoria)
SELECT 'Criollo de Hoja (Kg)', 'Criollos tradicionales con grasa', 3500.00, 5, c.id_categoria
FROM categorias c WHERE c.nombre = 'Facturería'
AND NOT EXISTS (SELECT 1 FROM productos p WHERE p.nombre = 'Criollo de Hoja (Kg)');

INSERT INTO productos (nombre, descripcion, precio, stock_minimo, id_categoria)
SELECT 'Medialuna de Manteca', 'Medialunas dulces de manteca', 450.00, 20, c.id_categoria
FROM categorias c WHERE c.nombre = 'Facturería'
AND NOT EXISTS (SELECT 1 FROM productos p WHERE p.nombre = 'Medialuna de Manteca');

INSERT INTO productos (nombre, descripcion, precio, stock_minimo, id_categoria)
SELECT 'Torta Selva Negra', 'Torta con crema y cerezas', 18000.00, 2, c.id_categoria
FROM categorias c WHERE c.nombre = 'Repostería'
AND NOT EXISTS (SELECT 1 FROM productos p WHERE p.nombre = 'Torta Selva Negra');

INSERT INTO movimientos (id_producto, tipo_movimiento, cantidad, fecha, observacion)
SELECT p.id_producto, 'ENTRADA', 30, '2026-09-10 07:00:00', 'Horneado producción mañana'
FROM productos p WHERE p.nombre = 'Pan Francés (Kg)'
AND NOT EXISTS (SELECT 1 FROM movimientos m WHERE m.id_producto=p.id_producto AND m.observacion='Horneado producción mañana');

INSERT INTO movimientos (id_producto, tipo_movimiento, cantidad, fecha, observacion)
SELECT p.id_producto, 'SALIDA', 12, '2026-09-10 10:30:00', 'Venta mostrador'
FROM productos p WHERE p.nombre = 'Pan Francés (Kg)'
AND NOT EXISTS (SELECT 1 FROM movimientos m WHERE m.id_producto=p.id_producto AND m.observacion='Venta mostrador');

-- Roles de base de datos (MySQL 8.0 o superior).
CREATE ROLE IF NOT EXISTS 'rol_admin';
CREATE ROLE IF NOT EXISTS 'rol_operador';
GRANT ALL PRIVILEGES ON panstock.* TO 'rol_admin';
GRANT SELECT ON panstock.* TO 'rol_operador';
GRANT INSERT, UPDATE ON panstock.productos TO 'rol_operador';
GRANT INSERT ON panstock.movimientos TO 'rol_operador';

-- Crear usuarios de ejemplo y asignarles los roles.
-- Cambiar las contraseñas antes de utilizar en un entorno real.
CREATE USER IF NOT EXISTS 'panstock_admin'@'localhost' IDENTIFIED BY 'Cambiar_Admin_2026!';
CREATE USER IF NOT EXISTS 'panstock_operador'@'localhost' IDENTIFIED BY 'Cambiar_Operador_2026!';
GRANT 'rol_admin' TO 'panstock_admin'@'localhost';
GRANT 'rol_operador' TO 'panstock_operador'@'localhost';
SET DEFAULT ROLE 'rol_admin' TO 'panstock_admin'@'localhost';
SET DEFAULT ROLE 'rol_operador' TO 'panstock_operador'@'localhost';

-- Consulta de productos con stock calculado a partir de los movimientos.
SELECT p.id_producto, p.nombre, p.precio, p.stock_minimo,
       COALESCE(SUM(CASE
           WHEN m.tipo_movimiento = 'ENTRADA' THEN m.cantidad
           WHEN m.tipo_movimiento = 'SALIDA' THEN -m.cantidad
           ELSE 0 END), 0) AS stock_actual,
       CASE WHEN COALESCE(SUM(CASE
           WHEN m.tipo_movimiento = 'ENTRADA' THEN m.cantidad
           WHEN m.tipo_movimiento = 'SALIDA' THEN -m.cantidad
           ELSE 0 END), 0) < p.stock_minimo
       THEN 'BAJO' ELSE 'OK' END AS estado_stock
FROM productos p
LEFT JOIN movimientos m ON m.id_producto = p.id_producto
GROUP BY p.id_producto, p.nombre, p.precio, p.stock_minimo
ORDER BY p.nombre;
