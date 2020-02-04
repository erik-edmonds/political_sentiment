#!/bin/bash

curl -X PUT localhost:8083/connectors/mongo_connector/config -H "Content-Type: application/json" -d '{
	"name": "mongo_connector",
	"config": {
		"connector.class":"MongoSourceConnector",
		#"key.converter":"org.apache.kafka.connect.storage.StringConverter",
		#"value.converter":"org.apache.kafka.connect.storage.StringConverter",
		"connection.uri": "mongodb://erikedmonds:Edmonds25@localhost:27017",
		"database":"test_database",
		"collection":"test_collection",
		"topic.prefix":""
	}
}'
