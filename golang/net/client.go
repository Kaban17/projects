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

	// Start reader goroutine
	go func() {
		reader := bufio.NewReader(conn)
		for {
			message, err := reader.ReadString('\n')
			if err != nil {
				log.Println("Read error:", err)
				return
			}
			fmt.Printf("[Server] %s", message)
		}
	}()

	// Start writer
	scanner := bufio.NewScanner(os.Stdin)
	fmt.Println("Enter messages to send (or 'exit' to quit):")
	for scanner.Scan() {
		text := scanner.Text()
		if text == "exit" {
			return
		}

		// Create proper JSON message
		id, _ := strconv.Atoi(clientID)
		msg := Message{
			ID:      id,
			Name:    "Client-" + clientID,
			Content: text,
		}

		jsonData, err := json.Marshal(msg)
		if err != nil {
			log.Println("JSON marshal error:", err)
			continue
		}

		// Send with newline delimiter
		if _, err := fmt.Fprintf(conn, "%s\n", jsonData); err != nil {
			log.Println("Send error:", err)
			return
		}
	}
}
