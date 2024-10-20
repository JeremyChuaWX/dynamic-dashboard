CREATE TABLE IF NOT EXISTS operations (
    op_id INTEGER PRIMARY KEY, -- A random number starts with 4 for the operation
    subject_id INTEGER NOT NULL, -- A random number starts with 1 for the patient
    hadm_id INTEGER NOT NULL, -- A random number starts with 2 for hospital admission
    case_id INTEGER, -- A linker to VitalDB Open Dataset
    opdate TIMESTAMP, -- Operation date
    age INTEGER, -- Age of the patient on the operation date
    sex CHAR(1) CHECK (sex IN ('M', 'F')), -- Sex of the patient
    weight NUMERIC, -- Weight measured before operation
    height NUMERIC, -- Height measured before operation
    asa INTEGER CHECK (asa IN (1, 2, 3, 4, 5)), -- American Society of Anesthesiologists physical status classification
    emop BOOLEAN, -- Emergency of the operation
    department VARCHAR(255), -- Surgical department for admission
    antype VARCHAR(50), -- Anesthesia Type (General / Neuraxial / Regional / MAC)
    icd10_pcs VARCHAR(50), -- ICD-10 Procedure Coding System code
    orin_time TIMESTAMP, -- The time for entering the operating room
    orout_time TIMESTAMP, -- The time for leaving the operating room
    opstart_time TIMESTAMP, -- The time for starting the operation
    opend_time TIMESTAMP, -- The time for finishing the operation
    admission_time TIMESTAMP, -- The time for hospital admission
    discharge_time TIMESTAMP, -- The time for hospital discharge
    anstart_time TIMESTAMP, -- The time for starting anaesthesia
    anend_time TIMESTAMP, -- The time for finishing anaesthesia
    cpbon_time TIMESTAMP, -- The time for starting cardiopulmonary bypass
    cpboff_time TIMESTAMP, -- The time for finishing cardiopulmonary bypass
    icuin_time TIMESTAMP, -- The time for ICU admission after surgery
    icuout_time TIMESTAMP, -- The time for ICU discharge after surgery
    inhosp_death_time TIMESTAMP -- The time for in-hospital death
);

CREATE TABLE IF NOT EXISTS diagnosis (
    subject_id INTEGER, -- The patient identifier defined in the operations table
    chart_time TIMESTAMP, -- The time for the diagnosis recorded
    icd10_cm VARCHAR(50) -- ICD-10 Diagnosis Code
);

CREATE TABLE IF NOT EXISTS vitals (
    subject_id INTEGER, -- The patient identifier defined in the operations table
    chart_time TIMESTAMP, -- The time for the measurement recorded
    item_name VARCHAR(255), -- Label for the measurement
    value NUMERIC, -- Measured value
    op_id INTEGER -- Operation identifier defined in the operations table
);

CREATE TABLE IF NOT EXISTS ward_vitals (
    subject_id INTEGER, -- The patient identifier defined in the operations table
    chart_time TIMESTAMP, -- The time for the measurement recorded
    item_name VARCHAR(255), -- Label for the measurement
    value NUMERIC -- Measured value
);

CREATE TABLE IF NOT EXISTS labs (
    subject_id INTEGER, -- The patient identifier defined in the operations table
    chart_time TIMESTAMP, -- The time for the measurement recorded
    item_name VARCHAR(255), -- Label for the measurement
    value NUMERIC -- Measured value
);

CREATE TABLE IF NOT EXISTS medications (
    subject_id INTEGER, -- The patient identifier defined in the operations table
    chart_time TIMESTAMP, -- The time for the measurement recorded
    drug_name VARCHAR(255), -- Name of the medication
    route VARCHAR(50) -- Route for the medication (po/iv/ex)
);

CREATE INDEX IF NOT EXISTS idx_operations_subject_id ON operations(subject_id);
CREATE INDEX IF NOT EXISTS idx_diagnosis_subject_id ON diagnosis(subject_id);
CREATE INDEX IF NOT EXISTS idx_vitals_subject_id ON vitals(subject_id);
CREATE INDEX IF NOT EXISTS idx_vitals_op_id ON vitals(op_id);
CREATE INDEX IF NOT EXISTS idx_ward_vitals_subject_id ON ward_vitals(subject_id);
CREATE INDEX IF NOT EXISTS idx_labs_subject_id ON labs(subject_id);
CREATE INDEX IF NOT EXISTS idx_medications_subject_id ON medications(subject_id);
