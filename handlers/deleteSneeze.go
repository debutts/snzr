package handlers

import (
	"net/http"
	"snzr/models"

	"github.com/gin-gonic/gin"
)

func DeleteSneeze(c *gin.Context) {
	id := c.Param("id")
	for i, s := range sneezeHistory {
		if(s.Id == id) {
			sneezeHistory = append(sneezeHistory[:i], sneezeHistory[i+1:]...)
			c.IndentedJSON(http.StatusOK)
			return
		}
		c.IndentedJSON(http.StatusNotFound, gin.H{"message": "sneeze not found"})
		return
	}