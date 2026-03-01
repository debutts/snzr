package main

import (
	"github.com/gin-gonic/gin"
	"snzr/handlers"
)

func main() {
	router := gin.Default()
	router.GET("/sneeze", handlers.GetSneezes)
	router.GET("/sneeze/:id", handlers.GetSneeze)
	router.PUT("/sneeze/:id", handlers.UpdateSneeze)
	router.POST("/sneeze", handlers.CreateSneeze)
	router.DELETE("/sneeze/:id", handlers.DeleteSneeze)

	router.Run("localhost:8080")
}