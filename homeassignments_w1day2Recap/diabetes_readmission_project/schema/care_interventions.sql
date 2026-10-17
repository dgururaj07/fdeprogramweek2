CREATE TABLE IF NOT EXISTS care_interventions (
    intervention_id BIGSERIAL PRIMARY KEY,
    encounter_id BIGINT NOT NULL UNIQUE REFERENCES patient_encounters(encounter_id) ON DELETE CASCADE,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING_REVIEW'
        CHECK (status IN (
            'PENDING_REVIEW',
            'ASSIGNED',
            'CONTACTED',
            'FOLLOW_UP_SCHEDULED',
            'CLOSED'
        )),
    assigned_to VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_care_interventions_status ON care_interventions (status);
