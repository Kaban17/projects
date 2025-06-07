package main

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

func CountCharacters(str string) map[string]int {
	// Step 1: Create a map to store character counts
	counts := make(map[string]int)

	// Step 2: Iterate over each character in the string
	for _, char := range str {
		// Step 3: Increment the count for the current character
		counts[string(char)]++
	}

	return counts
}
func main() {
	http.HandleFunc("/ws", handleWebSocket)
	http.HandleFunc("/", serveHome)
	http.HandleFunc("/client.html", serveClient)

	log.Println("Server started on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func serveHome(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "index.html")
}

func serveClient(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "client.html")
}
func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("WebSocket upgrade error:", err)
		return
	}
	defer conn.Close()

	for {
		// Читаем сообщение как JSON объект
		var msg map[string]interface{}
		if err := conn.ReadJSON(&msg); err != nil {
			log.Println("Read error:", err)
			return
		}

		// Валидация полей
		id, ok := msg["id"].(float64)
		if !ok {
			log.Println("Invalid ID format")
			continue
		}

		content, ok := msg["content"].(string)
		if !ok {
			log.Println("Invalid content format")
			continue
		}
		ans := CountCharacters(content)
		// Формируем ответ
		response := map[string]interface{}{
			"status":   "success",
			"clientId": int(id),
			"count":    ans,
		}

		// Отправляем ответ
		if err := conn.WriteJSON(response); err != nil {
			log.Println("Write error:", err)
			return
		}
	}
}
