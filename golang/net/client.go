package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
)

type Message struct {
	ID      int    `json:"id"`
	Name    string `json:"name"`
	Content string `json:"content"`
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: client <client-id>")
	}
	clientID := os.Args[1]

	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		log.Fatal("Connection error:", err)
	}
	defer conn.Close()

	// Получаем ID клиента
	id, err := strconv.Atoi(clientID)
	if err != nil {
		log.Fatal("Invalid client ID:", err)
	}

	// Читаем сообщение от пользователя
	fmt.Print("Enter your message: ")
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	messageText := scanner.Text()

	// Формируем сообщение
	msg := Message{
		ID:      id,
		Name:    "Client-" + clientID,
		Content: messageText,
	}

	// Кодируем в JSON
	jsonData, err := json.Marshal(msg)
	if err != nil {
		log.Fatal("JSON marshal error:", err)
	}

	// Отправляем сообщение
	_, err = conn.Write(append(jsonData, '\n'))
	if err != nil {
		log.Fatal("Send error:", err)
	}

	// Читаем ответ
	reader := bufio.NewReader(conn)
	response, err := reader.ReadString('\n')
	if err != nil {
		log.Fatal("Read error:", err)
	}

	fmt.Printf("\nServer response: %s", response)

	// Соединение закроется автоматически через defer
}
