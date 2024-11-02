CREATE TABLE IF NOT EXISTS layouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    layout TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
