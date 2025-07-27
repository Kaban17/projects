package main

import (
	"fmt"
	"math/rand"
	"time"
)

func Shuffle[T any](slice []T) {
	rand.New(rand.NewSource(time.Now().UnixNano()))
	for i := len(slice) - 1; i > 0; i-- {
		j := rand.Intn(i + 1)
		slice[i], slice[j] = slice[j], slice[i]
	}
}

func main() {
	// Example usage
	numbers_string := []string{"first", "second", "third", "fourth", "fifth"}
	Shuffle(numbers_string)
	fmt.Println(numbers_string)
	numbers_int := []float64{1, 2, 3, 4, 5}
	Shuffle(numbers_int)
	fmt.Println(numbers_int)
}
