package main

import (
	"fmt"
	"sync"
	"time"
)

type Worker struct {
	id    int
	wg    *sync.WaitGroup
	tasks <-chan string
	quit  chan struct{}
}

func (w *Worker) start() {
	defer w.wg.Done()
	for {
		select {
		case task, ok := <-w.tasks:
			if !ok {
				return
			}
			fmt.Printf("Worker %d: %s\n", w.id, task)
		case <-w.quit:
			return
		}
	}
}

type WorkerPool struct {
	tasks        chan string
	wg           sync.WaitGroup
	mu           sync.Mutex
	workers      map[int]*Worker
	addWorker    chan struct{}
	removeWorker chan int
	quit         chan struct{}
	nextId       int
}

func NewWorkerPool() *WorkerPool {
	return &WorkerPool{
		tasks:        make(chan string, 100),
		workers:      make(map[int]*Worker),
		addWorker:    make(chan struct{}),
		removeWorker: make(chan int),
		quit:         make(chan struct{}),
	}
}
func (wp *WorkerPool) Run() {
	for {
		select {
		case <-wp.addWorker:
			wp.mu.Lock()
			id := wp.nextId
			wp.nextId++
			w := &Worker{
				id:    id,
				wg:    &wp.wg,
				tasks: wp.tasks,
				quit:  make(chan struct{}),
			}
			wp.workers[id] = w
			wp.wg.Add(1)
			go w.start()
			fmt.Printf("Worker %d added\n", id)
			wp.mu.Unlock()
		case id := <-wp.removeWorker:
			wp.mu.Lock()
			if w, exists := wp.workers[id]; exists {
				close(w.quit)
				delete(wp.workers, id)
				fmt.Printf("Worker %d removed\n", id)
			} else {
				fmt.Printf("Worker %d not found\n", id)
			}
			wp.mu.Unlock()
		case <-wp.quit:
			wp.mu.Lock()
			for id, work := range wp.workers {
				close(work.quit)
				delete(wp.workers, id)
			}

			wp.mu.Unlock()
			wp.wg.Wait()
			close(wp.tasks)
			return
		}
	}
}
func (wp *WorkerPool) AddWorker() {
	wp.addWorker <- struct{}{}
}
func (wp *WorkerPool) RemoveWorker(id int) {
	wp.removeWorker <- id
}

func (wp *WorkerPool) SubmitTask(task string) {
	wp.tasks <- task
}
func (wp *WorkerPool) Stop() {
	wp.quit <- struct{}{}
}
func main() {
	pool := NewWorkerPool()
	go pool.Run()

	// Добавляем начальных воркеров
	pool.AddWorker()
	pool.AddWorker()

	// Отправляем задачи
	for i := 0; i < 5; i++ {
		pool.SubmitTask(fmt.Sprintf("task_%d", i))
	}

	// Добавляем еще воркера через 1 секунду
	time.Sleep(time.Second)
	pool.AddWorker()

	// Удаляем первого воркера через 2 секунды
	time.Sleep(time.Second)
	pool.RemoveWorker(0)

	// Отправляем еще задач
	for i := 5; i < 10; i++ {
		pool.SubmitTask(fmt.Sprintf("task_%d", i))
	}

	// Даем время на обработку
	time.Sleep(2 * time.Second)
	pool.Stop()
}
