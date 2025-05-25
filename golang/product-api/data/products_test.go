package data

import (
	"testing"
)

func TestCheckValidation(t *testing.T) {
	// Test case with missing required 'Name'
	p := &Product{} // This should now work
	err := p.Validate()
	if err == nil {
		t.Fatal("expected validation error, got nil")
	}

	// Test case with valid data
	p = &Product{
		Name:        "Test Product",
		Description: "A valid description",
		Price:       19.99,
		SKU:         "ksu-sku-sku",
	}
	err = p.Validate()
	if err != nil {
		t.Fatal("expected no error, got:", err)
	}
}
