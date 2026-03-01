package handlers

import (
	"net/http"
	"snzr/models"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

func createSneeze(c *gin.Context) {
	var request models.CreateSneezeRequest

	if err := c.BindJSON(&request); err != nil {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var newSneeze models.Sneeze = {
		Id: uuid.New().String(),
		OccurredAt: request.OccurredAt | time.Now(),
		Notes: request.Notes,
		Volume: request.Volume,
		Location: request.Location

	}

	sneezeHistory = append(sneezeHistory, newSneeze)

	c.IndentedJSON(http.StatusCreated, newSneeze)
}