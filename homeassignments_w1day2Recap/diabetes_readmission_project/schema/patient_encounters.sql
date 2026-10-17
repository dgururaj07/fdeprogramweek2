CREATE TABLE patient_encounters (
    encounter_id       BIGINT PRIMARY KEY,
    patient_nbr         BIGINT NOT NULL,
    age                 VARCHAR(10) NOT NULL,   -- e.g. '[70-80)'
    time_in_hospital    SMALLINT NOT NULL,
    number_inpatient    SMALLINT NOT NULL,
    number_emergency    SMALLINT NOT NULL,
    number_outpatient   SMALLINT NOT NULL,
    num_medications     SMALLINT NOT NULL,
    readmitted          VARCHAR(3) NOT NULL,    -- 'NO', '<30', '>30'
    risk_score          NUMERIC(5,2),           -- computed score, e.g. 0.00-100.00
    risk_level          VARCHAR(10),            -- e.g. 'Low', 'Medium', 'High'
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT valid_risk_level CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH'))
);

CREATE INDEX idx_patient_encounters_patient_nbr ON patient_encounters (patient_nbr);
CREATE INDEX idx_patient_encounters_readmitted  ON patient_encounters (readmitted);
