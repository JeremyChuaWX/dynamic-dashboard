CREATE INDEX IF NOT EXISTS idx_operations_subject_id ON operations(subject_id);
CREATE INDEX IF NOT EXISTS idx_diagnosis_subject_id ON diagnosis(subject_id);
CREATE INDEX IF NOT EXISTS idx_vitals_subject_id ON vitals(subject_id);
CREATE INDEX IF NOT EXISTS idx_vitals_op_id ON vitals(op_id);
CREATE INDEX IF NOT EXISTS idx_ward_vitals_subject_id ON ward_vitals(subject_id);
CREATE INDEX IF NOT EXISTS idx_labs_subject_id ON labs(subject_id);
CREATE INDEX IF NOT EXISTS idx_medications_subject_id ON medications(subject_id);
