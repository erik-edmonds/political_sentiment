#!/bin/bash

curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
	"name":"mongo_connector",
	"config": {
      		"tasks.max":1,
      		"connector.class":"com.mongodb.kafka.connect.MongoSourceConnector",
      		"key.converter":"org.apache.kafka.connect.storage.StringConverter",
      		"value.converter":"org.apache.kafka.connect.storage.StringConverter",
      		"connection.uri":"mongodb://erikedmonds:Edmonds25@localhost:27017",
      		"database":"test_database",
      		"collection":"test_collection",
      		"pipeline":"[{\"$match\": { \"$and\": [ { \"updateDescription.updatedFields.quantity\" : { \"$lte\": 5 } }, {\"operationType\": \"update\"}]}}]", 
		"topic.prefix": ""
	}
}'
