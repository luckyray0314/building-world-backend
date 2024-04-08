setup_postgres:
	docker run --name=risoftware -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=1234 -e POSTGRES_HOST_AUTH_METHOD=trust -e POSTGRES_DB=risoftware -p 5432:5432 -d postgres:13.1-alpine

postgres:
	docker start risoftware

enter_postgres:
	docker exec -it risoftware psql -U postgres -d risoftware 

delete_all_postgres:
	docker exec -it risoftware psql -U postgres -d risoftware -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

populate_db: delete_all_postgres
	python fake.py
	