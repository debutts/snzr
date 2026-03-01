package domain/sneeze/handlers

import (
	"net/http"
	"snzr/domains/sneeze/models"

	"github.com/gin-gonic/gin"
)

func UpdateSneeze(c *gin.Context) {
	id := c.Param("id")
	s, ok := sneezeHistory[id]
	if !ok {
		c.IndentedJSON(http.StatusNotFound, gin.H{"message": "sneeze not found"})
		return
	}
	var request models.Sneeze
	if err := c.ShouldBindJSON(&request); err != nil {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	s.OccurredAt = request.OccurredAt
	s.Notes = request.Notes
	s.Volume = request.Volume
	s.Location = request.Location
	sneezeHistory[id] = s
	c.IndentedJSON(http.StatusOK, s)
}