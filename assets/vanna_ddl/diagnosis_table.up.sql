CREATE TABLE IF NOT EXISTS diagnosis (
    subject_id INTEGER, -- The patient identifier defined in the operations table
    chart_time TIMESTAMP, -- The time for the diagnosis recorded
    icd10_cm VARCHAR(50) -- ICD-10 Diagnosis Code
);
