CREATE TABLE IF NOT EXISTS medications (
    subject_id INTEGER, -- The patient identifier defined in the operations table
    chart_time TIMESTAMP, -- The time for the measurement recorded
    drug_name VARCHAR(255), -- Name of the medication
    route VARCHAR(50) -- Route for the medication (po/iv/ex)
);
