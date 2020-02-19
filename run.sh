#!/bin/bash

spark-submit --master local[0] \
	--packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 \
	tensorflow_connector.py \
	1000
