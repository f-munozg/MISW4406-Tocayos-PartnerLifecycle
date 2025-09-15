-- Script de inicialización de la base de datos para Partner Lifecycle Management

-- Crear esquema si no existe
CREATE SCHEMA IF NOT EXISTS partner_lifecycle;

-- Crear tabla de partnerships
CREATE TABLE IF NOT EXISTS partnerships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_marca UUID NOT NULL,
    id_partner UUID NOT NULL,
    tipo_partnership VARCHAR(50) NOT NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'iniciando',
    nivel VARCHAR(50) NOT NULL DEFAULT 'bronce',
    fecha_inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin TIMESTAMP,
    fecha_ultima_actividad TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    terminos_contrato TEXT,
    comision_porcentaje FLOAT NOT NULL DEFAULT 0.0,
    metas_mensuales INTEGER NOT NULL DEFAULT 0,
    beneficios_adicionales TEXT,
    notas TEXT,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_partnerships_id_marca ON partnerships(id_marca);
CREATE INDEX IF NOT EXISTS idx_partnerships_id_partner ON partnerships(id_partner);
CREATE INDEX IF NOT EXISTS idx_partnerships_estado ON partnerships(estado);
CREATE INDEX IF NOT EXISTS idx_partnerships_tipo ON partnerships(tipo_partnership);
CREATE INDEX IF NOT EXISTS idx_partnerships_nivel ON partnerships(nivel);
CREATE INDEX IF NOT EXISTS idx_partnerships_fecha_creacion ON partnerships(fecha_creacion);

-- Insertar datos de ejemplo
INSERT INTO partnerships (id, id_marca, id_partner, tipo_partnership, estado, nivel, terminos_contrato, comision_porcentaje, metas_mensuales, beneficios_adicionales) VALUES
    (gen_random_uuid(), gen_random_uuid(), gen_random_uuid(), 'marca_afiliado', 'activo', 'plata', 'Contrato de afiliación estándar', 15.0, 100, 'Descuentos especiales, material promocional'),
    (gen_random_uuid(), gen_random_uuid(), gen_random_uuid(), 'marca_influencer', 'en_negociacion', 'bronce', 'Negociación en curso', 10.0, 50, 'Productos gratuitos para review');
