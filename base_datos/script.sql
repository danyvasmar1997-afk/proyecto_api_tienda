
DROP DATABASE IF EXISTS api_tienda;
CREATE DATABASE api_tienda;
USE api_tienda;


CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(150)
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    id_categoria INT NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE CASCADE
);

CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_pago DECIMAL(10, 2) NOT NULL CHECK (total_pago >= 0),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
);


INSERT INTO categorias (nombre, descripcion) VALUES
('Componentes de PC', 'Procesadores, tarjetas graficas, memorias RAM y almacenamiento'),
('Perifericos', 'Teclados, mouses, diademas y monitores para computadoras'),
('Audio', 'Audifonos inalambricos, parlantes y barras de sonido'),
('Smartphones y Accesorios', 'Teléfonos celulares, cargadores y estuches');

INSERT INTO productos (nombre, precio, stock, id_categoria) VALUES
-- Componentes de PC 
('Procesador AMD Ryzen 5 5600X', 850000.00, 10, 1),
('Procesador Intel Core i7-12700K', 1450000.00, 6, 1),
('Tarjeta Grafica RTX 4060 Ti', 2300000.00, 4, 1),
('Memoria RAM Corsair 16GB DDR4', 280000.00, 25, 1),
('Disco Estado Solido SSD NVMe 1TB', 350000.00, 20, 1),

-- Perifericos
('Teclado Mecanico Logitech G413', 320000.00, 15, 2),
('Mouse Gamer Razer DeathAdder V2', 190000.00, 30, 2),
('Monitor Gamer Asus 24" 165Hz', 950000.00, 8, 2),
('Diadema HyperX Cloud Stinger', 220000.00, 18, 2),
('Camara Web Logitech C920 HD', 380000.00, 12, 2),

-- Audio
('Audifonos Sony WH-1000XM4 Bluetooth', 1100000.00, 5, 3),
('Audifonos Apple AirPods 3ra Gen', 900000.00, 14, 3),
('Parlante Portatil JBL Flip 6', 490000.00, 22, 3),
('Barra de Sonido Samsung T450', 650000.00, 7, 3),
('Microfono USB Blue Yeti', 620000.00, 9, 3),

-- Smartphones y Accesorios
('Celular Samsung Galaxy S23 Ultra', 4800000.00, 3, 4),
('Celular Xiaomi Redmi Note 12 Pro', 1200000.00, 16, 4),
('Cargador Rápido Anker 20W USB-C', 75000.00, 40, 4),
('Batería Portátil Baseus 20000mAh', 160000.00, 25, 4),
('Soporte de Celular para Escritorio', 35000.00, 50, 4);

SELECT * FROM productos;

-- Insertar Pedidos
INSERT INTO pedidos (id_producto, cantidad, total_pago) VALUES
(1, 1, 850000.00),  -- 1 Procesador
(7, 2, 380000.00),  -- 2 Mouses 
(18, 3, 225000.00); -- 3 Cargadores 

SELECT ped.id_pedido, prod.nombre AS producto, cat.nombre AS categoria_producto,ped.cantidad, ped.total_pago,ped.fecha_pedido
FROM pedidos ped
INNER JOIN productos prod ON ped.id_producto = prod.id_producto
INNER JOIN categorias cat ON prod.id_categoria = cat.id_categoria;