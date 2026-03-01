package domain/sneeze/models

import "time"

type Sneeze struct {
	Id        string     `json:"id"`
	UserId    string     `json:"user_id"`
	Notes     *string    `json:"notes"`
	OccurredAt time.Time  `json:"occurred_at"`
	Location  *string    `json:"location"`
	Volume    *int       `json:"volume"`
}