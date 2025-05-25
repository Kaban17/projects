package handlers

import (
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/nicholasjackson/building-microservices-youtube/product-api/data"
)

// swagger:route DELETE /products/{id} products deleteProduct
// Delete a product from the database
// responses:
//	201: noContentResponse
//	404: errorResponse
//	500: errorResponse

// DeleteProduct deletes a product from the database
func (p *Products) DeleteProduct(w http.ResponseWriter, r *http.Request) {
	// this always convert because of the router
	vars := mux.Vars(r)
	id, _ := strconv.Atoi(vars["id"])
	p.l.Println("Handler: Deleting product with ID", id)
	err := data.DeleteProduct(id)
	if err == data.ErrProductNotFound {
		p.l.Println("[ERROR] Deleting product with ID", id, "not found")
		http.Error(w, "Product not found", http.StatusNotFound)
		return
	}
	if err != nil {
		p.l.Println("[ERROR] Deleting product with ID", id, "failed")
		http.Error(w, "Product not found", http.StatusInternalServerError)
		return
	}
}
