import subprocess, pyspark
from pyspark.sql import SparkSession
from pyspark import SparkConf
from py4j import protocol

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
        print(df.show(n=50))
    except protocol.Py4JJavaError:
        print("Error.")
    