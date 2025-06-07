package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"math/rand"
	"net/http"
	"sync"
	"time"
)

// Отель
type Hotel struct {
	mu     sync.Mutex
	rooms  map[int]int // цена -> количество
	income int
	served int
}

func NewHotel() *Hotel {
	return &Hotel{
		rooms:  map[int]int{500: 4, 700: 2, 900: 2},
		income: 0,
		served: 0,
	}
}

func (h *Hotel) CheckIn(budget int) bool {
	h.mu.Lock()
	defer h.mu.Unlock()

	for price := 900; price >= 500; price -= 200 {
		if h.rooms[price] > 0 && budget >= price {
			h.rooms[price]--
			h.income += price
			h.served++
			return true
		}
	}
	return false
}

func (h *Hotel) Stats() (int, int, int, map[int]int) {
	totalClients := h.served + h.NotServed()
	return totalClients, h.served, h.income, h.rooms
}

func (h *Hotel) NotServed() int {
	return 0 // можно улучшить, но для примера оставим заглушку
}

var hotel = NewHotel()
var notServed int

func simulateClient() {
	budget := rand.Intn(1000)
	if !hotel.CheckIn(budget) {
		notServed++
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		tmpl, _ := template.ParseFiles("templates/index.html")
		tmpl.Execute(w, nil)
	})

	http.HandleFunc("/checkin", func(w http.ResponseWriter, r *http.Request) {
		go simulateClient()
		w.WriteHeader(http.StatusOK)
	})

	http.HandleFunc("/stats", func(w http.ResponseWriter, r *http.Request) {
		total, served, income, rooms := hotel.Stats()
		stats := map[string]interface{}{
			"Total":   total,
			"Served":  served,
			"Income":  income,
			"Rooms":   rooms,
			"Pending": notServed,
		}
		json.NewEncoder(w).Encode(stats)
	})

	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("static"))))

	fmt.Println("Сервер запущен на http://localhost:8080")
	http.ListenAndServe(":8080", nil)
}
