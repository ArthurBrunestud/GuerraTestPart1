-- ============================================================
-- TABLAS MAESTRAS (sin cambios)
-- ============================================================

CREATE TABLE mae_trabajadores (
    id            SERIAL PRIMARY KEY,
    dni           VARCHAR(8)   NOT NULL UNIQUE,
    nombre        VARCHAR(80)  NOT NULL,
    apellido      VARCHAR(80)  NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    activo        BOOLEAN      NOT NULL DEFAULT TRUE,
    creado_en     TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE mae_proveedores (
    id        SERIAL PRIMARY KEY,
    nombre    VARCHAR(150) NOT NULL UNIQUE,
    telefono  VARCHAR(20)  NULL,
    direccion TEXT         NULL,
    activo    BOOLEAN      NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE mae_productos (
    id            SERIAL PRIMARY KEY,
    nombre        VARCHAR(150)  NOT NULL UNIQUE,
    descripcion   TEXT          NULL,
    categoria     VARCHAR(80)   NOT NULL,
    marca         VARCHAR(80)   NULL,
    precio_compra NUMERIC(12,2) NOT NULL CHECK (precio_compra > 0),
    moneda        VARCHAR(10)   NOT NULL DEFAULT 'PEN',
    stock         INTEGER       NOT NULL DEFAULT 0 CHECK (stock >= 0),
    imagen_url    VARCHAR(255)  NULL,
    activo        BOOLEAN       NOT NULL DEFAULT TRUE,
    creado_en     TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE TABLE trs_movimientos_stock (
    id            SERIAL PRIMARY KEY,
    producto_id   INTEGER NOT NULL REFERENCES mae_productos(id),
    proveedor_id  INTEGER REFERENCES mae_proveedores(id),
    tipo          VARCHAR(10) NOT NULL,
    cantidad      INTEGER NOT NULL,
    stock_despues INTEGER NOT NULL,
    notas         TEXT,
    fecha         TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO mae_trabajadores (
    dni,
    nombre,
    apellido,
    password_hash
) VALUES (
    '71376979',
    'Grossman',
    'Bejarano Yato',
    'scrypt:32768:8:1$DiQHptBkIxCITV8C$289bfabc82ebf62cb3a35c2bbbbcb6d4a3d5ef5cf937157c854955635dd780af97ac75ca6ceb9fe04b8b08ff95761626c3387a0521d74f2fd72ba51788bf4f21'
);