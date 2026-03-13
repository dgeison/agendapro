-- Migration 001: Criação das tabelas do domínio core
-- AgendaPro - agendapro-dev

-- ENUM de status de sessão
CREATE TYPE session_status AS ENUM (
    'PENDENT_PAYMENT',
    'CONFIRMED',
    'CANCELLED'
);

-- Tabela: professors
CREATE TABLE IF NOT EXISTS professors (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    specialty   TEXT NOT NULL,
    hourly_rate NUMERIC(10, 2) NOT NULL CHECK (hourly_rate > 0),
    room_link   TEXT NOT NULL,
    cancellation_tolerance_minutes INTEGER NOT NULL CHECK (cancellation_tolerance_minutes >= 0),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabela: students
CREATE TABLE IF NOT EXISTS students (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name       TEXT NOT NULL,
    whatsapp   TEXT NOT NULL UNIQUE,
    email      TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabela: sessions
CREATE TABLE IF NOT EXISTS sessions (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    professor_id   UUID NOT NULL REFERENCES professors(id),
    student_id     UUID NOT NULL REFERENCES students(id),
    slot_start     TIMESTAMPTZ NOT NULL,
    slot_end       TIMESTAMPTZ NOT NULL,
    status         session_status NOT NULL DEFAULT 'PENDENT_PAYMENT',
    lock_expires_at TIMESTAMPTZ NOT NULL,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT slot_end_after_start CHECK (slot_end > slot_start)
);

-- Índices para consultas frequentes
CREATE INDEX IF NOT EXISTS idx_sessions_professor_slot
    ON sessions (professor_id, slot_start, slot_end);

CREATE INDEX IF NOT EXISTS idx_sessions_status
    ON sessions (status);
