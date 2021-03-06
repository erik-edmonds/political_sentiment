#!/bin/bash

curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
	"name": "postgres_connector",
	"config": {
		"connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
		"connection.url": "jdbc:postgresql://localhost:5432/data",
		"connection.user": "erikedmonds",
		"connection.password": "Edmonds25",
		"table.whitelist": "public.senate",
		"topic.prefix": "postgres-",
		"mode": "bulk"
	}
}'
