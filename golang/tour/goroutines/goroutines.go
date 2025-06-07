package main

import "fmt"

func main() {
	first := make(chan int)
	prev := first
	for i := 0; i < 1e6; i++ {
		next := make(chan int)

		go func(prev chan int) {
			next <- <-prev
		}(prev)
		prev = next
	}
	first <- 100
	fmt.Println(<-prev)
}
