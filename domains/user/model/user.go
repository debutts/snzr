package domain/user/model

type User struct {
	Id string `json:"id"`
	Name Name `json:"name"`
	Email string `json:"email"`
}