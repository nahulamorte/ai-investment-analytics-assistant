-- Created by Redgate Data Modeler (https://datamodeler.redgate-platform.com)
-- Last modification date: 2026-05-28 17:44:28.348

-- tables
-- Table: activo_financiero
CREATE TABLE activo_financiero (
    id_activo int  NOT NULL,
    nombre varchar(120)  NOT NULL,
    ticker varchar(10)  NOT NULL,
    tipo_activo varchar(50)  NOT NULL,
    CONSTRAINT activo_financiero_pk PRIMARY KEY (id_activo)
);

-- Table: cartera
CREATE TABLE cartera (
    id_cartera int  NOT NULL,
    cantidad decimal(18,6)  NOT NULL,
    id_activo int  NOT NULL,
    id_usuario int  NOT NULL,
    CONSTRAINT cartera_pk PRIMARY KEY (id_cartera)
);

-- Table: historial_precios
CREATE TABLE historial_precios (
    id_precio int  NOT NULL,
    precio_cierre decimal(18,4)  NOT NULL,
    fecha date  NOT NULL,
    id_activo int  NOT NULL,
    CONSTRAINT historial_precios_pk PRIMARY KEY (id_precio)
);

-- Table: usuario
CREATE TABLE usuario (
    id_usuario int  NOT NULL,
    nombre varchar(120)  NOT NULL,
    perfil_riesgo varchar(120)  NOT NULL,
    CONSTRAINT usuario_pk PRIMARY KEY (id_usuario)
);

-- foreign keys
-- Reference: cartera_activo_financiero (table: cartera)
ALTER TABLE cartera ADD CONSTRAINT cartera_activo_financiero
    FOREIGN KEY (id_activo)
    REFERENCES activo_financiero (id_activo)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;

-- Reference: cartera_usuario (table: cartera)
ALTER TABLE cartera ADD CONSTRAINT cartera_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES usuario (id_usuario)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;

-- Reference: historial_precios_activo_financiero (table: historial_precios)
ALTER TABLE historial_precios ADD CONSTRAINT historial_precios_activo_financiero
    FOREIGN KEY (id_activo)
    REFERENCES activo_financiero (id_activo)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;

-- End of file.

