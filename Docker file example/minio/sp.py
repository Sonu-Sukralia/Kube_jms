from pyspark import SparkContext
from pyspark.sql import SparkSession
#http://s3a-hl.s3a:9000 
spark= SparkSession.builder.getOrCreate()

def load_config(spark_context: SparkContext):
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.access.key', 'l9clBhS80ZudADoDQnSS')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.secret.key', '5mU3bwzCDejg8aR3qgqwK0eVEsk8gUyxW0p0Cz6h')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.path.sytle.acess', 'true')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.endpoint', "http://localhost:9090/browser")
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.connection.ssl.enabled', 'false')
    

load_config(spark.sparkContext)

dataframe = spark.read.json('s3a://test/*')
#orders.json
average = dataframe.agg({'amount':'avg'})

#average.write.format("csv").option("header", "true").save("s3a://test/json/")

average.show()


