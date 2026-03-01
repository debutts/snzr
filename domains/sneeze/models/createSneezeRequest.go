package domain/sneeze/models

import (
	"time"

	"github.com/google/uuid"
)

type CreateSneezeRequest struct {
	Notes      *string    `json:"notes"`
	OccurredAt *time.Time `json:"occurred_at"`
	Location   *string    `json:"location"`
	Volume     *int       `json:"volume"`
}

func (request CreateSneezeRequest) ToSneeze() Sneeze {
	occurredAt := time.Now()
	if request.OccurredAt != nil {
		occurredAt = *request.OccurredAt
	}
	return Sneeze{
		Id: uuid.New().String(),
		UserId: "1221", //todo: get user id from context
		Notes: request.Notes,
		OccurredAt: occurredAt,
		Location: request.Location,
		Volume: request.Volume,
	}
}