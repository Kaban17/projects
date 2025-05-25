check_install:
	which swag || GO11MODULE=off go get -u github.com/go-swagger/go-swagger/cmd/swagger
swagger: check_install
	GO11MODULE=on swagger generate spec -o ./swagger.yaml --scan-models
