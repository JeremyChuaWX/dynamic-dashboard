CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY,
    type VARCHAR(3) CHECK (type IN ('ddl', 'doc'))
);
