package handlers

import (
	"net/http"
	"snzr/models"

	"github.com/gin-gonic/gin"
)

func createSneeze(c *gin.Context) {
	var request models.CreateSneezeRequest

	if err := c.BindJSON(&request); err != nil {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var newSneeze models.Sneeze = request.ToSneeze()

	sneezeHistory = append(sneezeHistory, newSneeze)

	c.IndentedJSON(http.StatusCreated, newSneeze)
}