-- 1. Modificar la tabla 'cartera' existente para adaptarla a la foto de estado neto
-- Cambiamos el nombre de la columna 'cantidad' a 'cantidad_neta' para mayor precisión técnica
ALTER TABLE cartera RENAME COLUMN cantidad TO cantidad_neta;

-- Agregamos la columna para el cálculo del Precio Promedio Ponderado de Compra
ALTER TABLE cartera ADD COLUMN precio_promedio_compra DECIMAL(18, 4) NOT NULL DEFAULT 0;

-- Aseguramos un índice único para evitar que se duplique la combinación usuario-activo en la foto fija
ALTER TABLE cartera ADD CONSTRAINT unique_usuario_activo_cartera UNIQUE (id_usuario, id_activo);


-- 2. Crear la nueva tabla 'operaciones' (Ledger Transaccional Inmutable)
-- Respetamos estrictamente los nombres del modelo importado de Redgate: 'usuario' y 'activo_financiero'
CREATE TABLE operaciones (
    id_operacion SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_activo INT NOT NULL,
    tipo_operacion VARCHAR(10) NOT NULL CHECK (tipo_operacion IN ('COMPRA', 'VENTA')),
    cantidad DECIMAL(18, 6) NOT NULL,
    precio_ejecucion DECIMAL(18, 4) NOT NULL,
    fecha_operacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Establecemos las Claves Foráneas vinculadas a tu esquema real
    CONSTRAINT fk_operaciones_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_operaciones_activo
        FOREIGN KEY (id_activo) REFERENCES activo_financiero(id_activo) ON DELETE CASCADE
);