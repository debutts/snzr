package handlers

import (
	"net/http"
	"time"

	"snzr/models"

	"github.com/gin-gonic/gin"
)

func strPtr(s string) *string { return &s }
func intPtr(i int) *int       { return &i }

var sneezeHistory = map[string]models.Sneeze{
	"1": {Id: "1", Notes: nil, OccurredAt: time.Now().Add(-48 * time.Hour), Location: strPtr("Living room"), Volume: nil},
	"2": {Id: "2", Notes: strPtr("Dust"), OccurredAt: time.Now().Add(-24 * time.Hour), Location: strPtr("Office"), Volume: intPtr(2)},
	"3": {Id: "3", Notes: strPtr("Morning allergies"), OccurredAt: time.Now().Add(-2 * time.Hour), Location: strPtr("Kitchen"), Volume: intPtr(4)},
}

// GetSneezes lists sneezes.
func GetSneezes(c *gin.Context) {
	list := make([]models.Sneeze, 0, len(sneezeHistory))
	for _, s := range sneezeHistory {
		list = append(list, s)
	}
	c.IndentedJSON(http.StatusOK, list)
}