package models

import "time"

type Sneeze struct {
	Id        string     `json:"id"`
	Notes     *string    `json:"notes"`
	OccurredAt time.Time  `json:"occurred_at"`
	Location  *string    `json:"location"`
	Volume    *int       `json:"volume"`
}