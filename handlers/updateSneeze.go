package handlers

import (
	"net/http"
	"snzr/models"

	"github.com/gin-gonic/gin"
)

func UpdateSneeze(c *gin.Context) {
	id := c.Param("id")
	for i, s := range sneezeHistory {
		if(s.Id == id) {
			var request models.Sneeze
			if err := c.ShouldBindJSON(&request); err != nil {
				c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			s.OccurredAt = request.OccurredAt
			s.Notes = request.Notes
			s.Volume = request.Volume
			s.Location = request.Location
			c.IndentedJSON(http.StatusOK, s)
			return
		}
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "sneeze not found"})
	return
}