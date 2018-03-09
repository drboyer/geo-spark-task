"""Calculates how many of the points in a dataset occur within a given quadkey"""
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, DecimalType

def point_to_quadkey(row):
    import mercantile
    return str(mercantile.quadkey(int(row.lat), int(row.lon), 5))

if __name__ == '__main__':
    spark = SparkSession.builder.enableHiveSupport().getOrCreate()

    schema = StructType([
        StructField('lat', DecimalType()),
        StructField('lon', DecimalType()),
    ])

    # ideally you'd load this data from some remote source (HDFS/S3)
    points_df = spark.read.csv('/opt/spark/work-dir/points.csv', schema=schema, header=True)
    quadkeys = points_df.rdd.map(point_to_quadkey)
    quadkey_output = sorted(quadkeys.countByValue().items(), key=lambda x: x[1])

    print(quadkey_output)