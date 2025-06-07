package main

import (
	"fmt"
	"math"
)

type Shape interface {
	Area() float64
	Perimeter() float64
}
type Rectangle struct {
	width, height float64
}

func (r Rectangle) Area() float64 {
	return r.width * r.height
}
func (r Rectangle) Perimeter() float64 {
	return 2 * (r.width + r.height)
}

type Circle struct {
	radius float64
}

func (c Circle) Area() float64 {
	return math.Pi * c.radius * c.radius
}
func (c Circle) Perimeter() float64 {
	return 2 * math.Pi * c.radius
}
func PrintShapeInfo(s Shape) {
	fmt.Printf(
		"Тип: %T\nПлощадь: %.2f\nПериметр: %.2f\n\n",
		s, s.Area(), s.Perimeter(),
	)
}
func main() {
	r1 := Rectangle{width: 2.0, height: 2.0}
	d := Circle{radius: 2.5}
	PrintShapeInfo(r1)
	PrintShapeInfo(d)
}
