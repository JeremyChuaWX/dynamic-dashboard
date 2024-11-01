CREATE TABLE IF NOT EXISTS visualisations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question TEXT,
    sql_query TEXT,
    plotly_code TEXT
);
