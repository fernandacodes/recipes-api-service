dev:
	docker compose up db -d
	docker compose up app
dbclean:
	docker stop data-service-db-1
	docker rm data-service-db-1
	docker volume rm data-service_postgres_data
webclean:
	docker rm data-service-app-1
	docker rmi data-service-app
db:
	docker compose up db -d
app:
	docker compose up app
