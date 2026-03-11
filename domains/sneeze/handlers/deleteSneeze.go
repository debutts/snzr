package domain/sneeze/handlers

import (
	"net/http"

	"snzr/domains/sneeze/models"

	"github.com/gin-gonic/gin"
)

func DeleteSneeze(c *gin.Context) {
	id := c.Param("id")
	if _, ok := sneezeHistory[id]; !ok {
		c.IndentedJSON(http.StatusNotFound, gin.H{"message": "sneeze not found"})
		return
	}
	delete(sneezeHistory, id)
	c.IndentedJSON(http.StatusOK, nil)
}