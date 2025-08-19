package main

import (
	"context"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

type numRange struct {
	min int
	max int
}

func main() {
	var ranges rangeSlice
	var outputFile string
	var timeout int

	flag.StringVar(&outputFile, "file", "primes.txt", "name of the output file")
	flag.IntVar(&timeout, "timeout", 10, "timeout in seconds")
	flag.Var(&ranges, "range", "numeric range (e.g., 1:100)")
	flag.Parse()

	if len(ranges) == 0 {
		fmt.Println("Please provide at least one range.")
		os.Exit(1)
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(timeout)*time.Second)
	defer cancel()

	primesCh := make(chan int)
	var wg sync.WaitGroup

	for _, r := range ranges {
		wg.Add(1)
		go findPrimes(ctx, r, primesCh, &wg)
	}

	var fileWg sync.WaitGroup
	fileWg.Add(1)
	go writeToFile(ctx, outputFile, primesCh, &fileWg)

	wg.Wait()
	close(primesCh)
	fileWg.Wait()

	fmt.Println("Processing complete.")
}

func findPrimes(ctx context.Context, r numRange, primesCh chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := r.min; i <= r.max; i++ {
		select {
		case <-ctx.Done():
			return
		default:
			if isPrime(i) {
				primesCh <- i
			}
		}
	}
}

func isPrime(n int) bool {
	if n <= 1 {
		return false
	}
	for i := 2; i*i <= n; i++ {
		if n%i == 0 {
			return false
		}
	}
	return true
}

func writeToFile(ctx context.Context, outputFile string, primesCh <-chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	file, err := os.Create(outputFile)
	if err != nil {
		fmt.Printf("Error creating file: %v\n", err)
		return
	}
	defer file.Close()

	for {
		select {
		case <-ctx.Done():
			fmt.Println("Timeout reached, stopping file writing.")
			return
		case prime, ok := <-primesCh:
			if !ok {
				return
			}
			_, err := file.WriteString(fmt.Sprintf("%d\n", prime))
			if err != nil {
				fmt.Printf("Error writing to file: %v\n", err)
				return
			}
		}
	}
}

type rangeSlice []numRange

func (r *rangeSlice) String() string {
	return fmt.Sprintf("%v", *r)
}

func (r *rangeSlice) Set(value string) error {
	parts := strings.Split(value, ":")
	if len(parts) != 2 {
		return fmt.Errorf("invalid range format: %s", value)
	}
	min, err := strconv.Atoi(parts[0])
	if err != nil {
		return fmt.Errorf("invalid min value: %s", parts[0])
	}
	max, err := strconv.Atoi(parts[1])
	if err != nil {
		return fmt.Errorf("invalid max value: %s", parts[1])
	}
	if min > max {
		return fmt.Errorf("min value cannot be greater than max value")
	}
	*r = append(*r, numRange{min, max})
	return nil
}
