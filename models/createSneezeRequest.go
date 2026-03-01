package models

import "time"

type CreateSneezeRequest struct {
	Notes     *string    `json:"notes"`
	OccurredAt *time.Time `json:"occurred_at"`
	Location  *string    `json:"location"`
	Volume    *int       `json:"volume"`
}