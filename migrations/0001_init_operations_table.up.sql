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
    asa INTEGER, -- American Society of Anesthesiologists physical status classification
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
