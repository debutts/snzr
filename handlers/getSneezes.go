package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"snzr/models"
)

var sneezeHistory = []models.Sneeze{
	{Id: "1", Notes: "Pollen season", OccurredAt: time.Now().Add(-48 * time.Hour), Location: "Living room", Volume: 3},
	{Id: "2", Notes: "Dust", OccurredAt: time.Now().Add(-24 * time.Hour), Location: "Office", Volume: 2},
	{Id: "3", Notes: "Morning allergies", OccurredAt: time.Now().Add(-2 * time.Hour), Location: "Kitchen", Volume: 4},
}

// GetSneezes lists sneezes.
func GetSneezes(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, sneezeHistory)
}