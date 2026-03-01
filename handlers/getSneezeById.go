package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// GetSneezes lists sneezes.
func GetSneeze(c *gin.Context) {
	id := c.Param("id")
	for _, s := range sneezeHistory {
		if(s.Id == id) {
			c.IndentedJSON(http.StatusOK, s)
			return
		}
	}

	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "sneeze not found"})
}