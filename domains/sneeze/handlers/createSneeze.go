package handlers

import (
	"net/http"
	"snzr/models"

	"github.com/gin-gonic/gin"
)

func CreateSneeze(c *gin.Context) {
	var request models.CreateSneezeRequest

	if err := c.BindJSON(&request); err != nil {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	newSneeze := request.ToSneeze()
	sneezeHistory[newSneeze.Id] = newSneeze

	c.IndentedJSON(http.StatusCreated, newSneeze)
}