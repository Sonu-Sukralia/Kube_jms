from pyspark import SparkContext
from pyspark.sql import SparkSession
#from pyspark.sql.types import StructType, StructField, LongType, DoubleType, StringType
#spark-3.5.2-bin-hadoop3
spark = SparkSession.builder \
    .appName("S3Example") \
    .master("local") \
    .config("spark.jars", "/usr/local/spark-3.5.2-bin-hadoop3/jars/hadoop-aws-3.3.4.jar,/usr/local/spark-3.5.2-bin-hadoop3/jars/aws-java-sdk-bundle-1.12.276.jar") \
    .getOrCreate()
#spark= SparkSession.builder.getOrCreate()
#http://s3a-hl.s3a:9000  spark://10.42.3.70:7077 http://localhost:9090

def load_config(spark_context: SparkContext):
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.access.key', 'l9clBhS80ZudADoDQnSS')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.secret.key', '5mU3bwzCDejg8aR3qgqwK0eVEsk8gUyxW0p0Cz6h')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.path.sytle.acess', 'true')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.endpoint', "http://s3a-hl.s3a:9000")
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.connection.ssl.enabled', 'false')

load_config(spark.sparkContext)

#dataframe = spark.read.json('s3a://test/orders.json')

dataframe = spark.read.json('s3a://test/orders.json')

average = dataframe.agg({'amount':'avg'})

average.write.format("csv").option("header", "true").save("s3a://test/json/")

average.show()