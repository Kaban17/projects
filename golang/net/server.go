package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"strings"
)

type Message struct {
	ID      int    `json:"id"`
	Name    string `json:"name"`
	Content string `json:"content"`
}

func main() {
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatal(err)
	}
	defer ln.Close()
	fmt.Println("TCP server listening on port 8080")

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Println("Accept error:", err)
			continue
		}
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	reader := bufio.NewReader(conn)

	for {
		// Read until newline
		message, err := reader.ReadString('\n')
		if err != nil {
			log.Println("Read error:", err)
			return
		}

		// Trim and check for empty message
		message = strings.TrimSpace(message)
		if message == "" {
			continue
		}

		// Parse JSON
		var msg Message
		if err := json.Unmarshal([]byte(message), &msg); err != nil {
			log.Printf("JSON parse error: %v | Raw: %s\n", err, message)
			sendResponse(conn, "ERROR: Invalid JSON format")
			continue
		}

		log.Printf("Received: %+v\n", msg)

		// Process and respond
		response := Message{
			ID:      msg.ID,
			Name:    fmt.Sprintf("Customer-%d", msg.ID),
			Content: fmt.Sprintf("Processed: %s", msg.Content),
		}

		if err := sendResponse(conn, response); err != nil {
			log.Println("Send error:", err)
			return
		}
	}
}

func sendResponse(conn net.Conn, data interface{}) error {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return err
	}
	_, err = fmt.Fprintf(conn, "%s\n", jsonData)
	return err
}
