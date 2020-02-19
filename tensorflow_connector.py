import subprocess, pyspark
from pyspark.sql import SparkSession
from pyspark import SparkConf
from py4j import protocol
from pyspark.sql.types import *

PATH = "test.tfrecord"

def create_session():
    """Dynamic URI?"""
    config = SparkConf().set("spark.jars","ecosystem/spark/spark-tensorflow-connector/target/spark-tensorflow-connector_2.11-1.10.0.jar")
    this = SparkSession \
        .builder \
        .appName("Data") \
        .config(conf=config) \
        .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/data.collection") \
        .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/data.collection") \
        .getOrCreate()
    return this
    
if __name__ == '__main__':
    try:
        this = create_session()
        df = this.read.format("mongo").load()
        
        df.write.format("tfrecords").option("recordType", "Example").save(PATH)
        print("SUCCESS!!")
    except protocol.Py4JJavaError:
        print("Error.")