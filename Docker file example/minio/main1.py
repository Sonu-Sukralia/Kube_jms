from pyspark import SparkContext
from pyspark.sql import SparkSession

spark= SparkSession.builder.getOrCreate()


#def load_config(spark_context: SparkContext):
#    spark_context._jsc.hadoopConfiguration().set('fs.s3a.access.key', 'MWl3E0EHYzzdePYZdZ1b')
 #   spark_context._jsc.hadoopConfiguration().set('fs.s3a.secret.key', 'Mc0C49TpSl3SgnUMRuv6RumdzOoOcjMCRLL0WVRq')
 #   spark_context._jsc.hadoopConfiguration().set('fs.s3a.path.sytle.acess', 'true')
  #  spark_context._jsc.hadoopConfiguration().set('fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
 #   spark_context._jsc.hadoopConfiguration().set('fs.s3a.endpoint', "http://s3a-hl.s3a:9000")
 #   spark_context._jsc.hadoopConfiguration().set('fs.s3a.connection.ssl.enabled', 'false')
    

#load_config(spark.SparkContext)

dataframe = spark.read.json('s3a://test/orders.json')

average = dataframe.agg({'amount':'avg'})

average.write.format("csv").option("header", "true").save(
    "s3a://test/json/")

average.show()


