CREATE TABLE IF NOT EXISTS labs (
    subject_id INTEGER, -- The patient identifier defined in the operations table
    chart_time TIMESTAMP, -- The time for the measurement recorded
    item_name VARCHAR(255), -- Label for the measurement
    value NUMERIC -- Measured value
);
