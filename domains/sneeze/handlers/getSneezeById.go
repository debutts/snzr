package domain/sneeze/handlers

import (
	"net/http"

	"snzr/domains/sneeze/models"

	"github.com/gin-gonic/gin"
)

// GetSneeze returns a single sneeze by ID.
func GetSneeze(c *gin.Context) {
	id := c.Param("id")
	if s, ok := sneezeHistory[id]; ok {
		c.IndentedJSON(http.StatusOK, s)
		return
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "sneeze not found"})
}