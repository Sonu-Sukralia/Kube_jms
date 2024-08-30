1.
1(a). Forcely delete pod if stuck in terminiating :-
      kubectl delete pod jupiter-spark-7469949554-s2p76 -n data-platform --grace-period 0 --force

1(b). Create service account and clusterrolebinding :-
      kubectl create serviceaccount spark -n data-platform
      kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=data-platform:spark --namespace=data-platform


2.  Jupyter Notebook Install
    https://hub.docker.com/repository/docker/sonusukralia/jupyterd/general
    Use Docker image in yaml :- sonusukralia/jupyterd:3.5
    kubectl apply -f Jupyternotebook.yaml
{
apiVersion: apps/v1
kind: Deployment
metadata:
   name: jupiter-spark
   namespace: data-platform
spec:
   replicas: 1
   selector:
      matchLabels:
         app: spark
   template:
      metadata:
         labels:
            app: spark
      spec:
         containers:
            - name: jupiter-spark-container
              image: sonusukralia/jupyterd:3.5
              imagePullPolicy: IfNotPresent
              ports:
              - containerPort: 8888
              env: 
              - name: JUPYTER_ENABLE_LAB
                value: "yes"
              resources:
                requests:
                  memory: "4Gi"  # Minimum memory requested
                limits:
                  memory: "6Gi"  # Maximum memory allowed
---
apiVersion: v1
kind: Service
metadata:
   name: jupiter-spark-svc
   namespace: data-platform
spec:
   type: NodePort
   selector:
      app: spark
   ports:
      - port: 8888
        targetPort: 8888
        nodePort: 30001
---
apiVersion: v1
kind: Service
metadata:
  name: jupiter-spark-driver-headless
spec:
  clusterIP: None
  selector:
    app: spark
}


3. Minio
3(a). https://hub.docker.com/repository/docker/sonusukralia/miniod/general
      Use Docker Image in yamo :- sonusukralia/miniod:3.5

3(b). Install Minio
Reference :- https://min.io/docs/minio/kubernetes/upstream/operations/installation.html
1. kubectl apply -k "github.com/minio/operator?ref=v5.0.15"
2. kubectl get pods -n minio-operator
3. kubectl get all -n minio-operator
4. Retrieve the Operator Console JWT for login
{
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: console-sa-secret
  namespace: minio-operator
  annotations:
    kubernetes.io/service-account.name: console-sa
type: kubernetes.io/service-account-token
EOF
SA_TOKEN=$(kubectl -n minio-operator  get secret console-sa-secret -o jsonpath="{.data.token}" | base64 --decode)
echo $SA_TOKEN
}

4. kubectl port-forward svc/console -n minio-operator 9090:9090
   https://192.168.29.15:9443/login
   http://localhost:9090/

SA_TOKEN=$(kubectl -n minio-operator  get secret console-sa-secret -o jsonpath="{.data.token}" | base64 --decode)
echo $SA_TOKEN



5. 
https://hub.docker.com/r/apache/spark/tags?page=&page_size=&ordering=&name=3.5.0

1.Dockerfile
FROM apache/spark:3.5.0-scala2.12-java11-python3-r-ubuntu
USER root
RUN useradd jovyan
RUN adduser jovyan root
WORKDIR /opt/spark/
COPY spark-defaults.conf /opt/spark/conf/
COPY aws-java-sdk-bundle-1.12.276.jar /opt/spark/jars/
COPY hadoop-aws-3.3.4.jar /opt/spark/jars/
COPY bcpkix-jdk18on-1.78.jar /opt/spark/jars/
COPY bcprov-jdk18on-1.78.jar /opt/spark/jars/

docker build -t sonusukralia/sparkp:3.5 .
docker push sonusukralia/sparkp:3.5



6. Spark_master_worker.yaml
kubectl apply -f Spark_master_worker.yaml
{
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: spark-master
  namespace: data-platform
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spark-master
  template:
    metadata:
      labels:
        app: spark-master
    spec:
      containers:
      - name: spark-master
        image: sonusukralia/sparkp:3.5
        imagePullPolicy: Always
        command: ["/opt/spark/bin/spark-class"]
        args: ["org.apache.spark.deploy.master.Master", "--host", "0.0.0.0"]
        ports:
        - containerPort: 7077  # Spark master port
        - containerPort: 8080  # Web UI port
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "1000m"

---

apiVersion: v1
kind: Service
metadata:
  name: spark-master-svc
  namespace: data-platform
spec:
  type: ClusterIP
  selector:
    app: spark-master
  ports:
  - name: spark-master
    port: 7077
    targetPort: 7077
  - name: spark-ui
    port: 8080
    targetPort: 8080

---

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: spark-worker
  namespace: data-platform
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spark-worker
  template:
    metadata:
      labels:
        app: spark-worker
    spec:
      containers:
      - name: spark-worker
        image: sonusukralia/sparkp:3.5
        imagePullPolicy: Always
        command: ["/opt/spark/bin/spark-class"]
        args: ["org.apache.spark.deploy.worker.Worker", "spark://spark-master-svc:7077"]
        ports:
        - containerPort: 8081  # Web UI port for worker
        resources:
          requests:
            memory: "4Gi"
            cpu: "500m"
          limits:
            memory: "5Gi"
            cpu: "4"


}


7. Jupyter_notebook_code.
File Name:- K8s_code_sparkmaster.ipynb

{
from pyspark.sql import SparkSession

# Kubernetes dashboard > Config And Storage > Secrets > s3a-env-configuration
#http://192.168.29.16:9090/browser/test login() :- E2XLJVLJHRZVUVLR & ZQ5BDKSIGDTIUI0CSRZYW22DRWKCTZLE

#Kubernetes dashboard > Service > Services > 
#Name (s3a-hl) 
#Labels(v1.min.io/tenant: s3a) Type(ClusterIP) Cluster IP(none) and Internal Endpoints(s3a-hl.data-platform:9000 TCP & s3a-hl.data-platform:0 TCP)
#http://s3a-hl.data-platform:9000

#http://192.168.29.16:9090 go to Minio console then create Object Browser and upload csv file and then create Access Keys
# "accessKey":"qUqE7TK7Xhkw9hS8DS4b","secretKey":"MeJYIY6s4X8P0SjYF7AsFkgf9AePLu837gndpAKS"

#To access spark cluser and jupyterlab.
#Jupyter Notebook    :- http://localhost:8888/lab/ :- no need token. 
#Jupyter Nodtebook   :- http://localhost:8888/lab/tree/K8s_code_sparkmaster.ipynb.
#Spark Master UI     :- http://10.43.175.33:8080/
#Application ID Logs :- http://10.42.3.220:8081/logPage/?appId=app-20240830140856-0003&executorId=0&logType=stderr
#For Driver host and driver bindaddress : Go to kubernetes dashboard(Namespace:-Data-platform) > 
#Workloads>Pods>jupiter-spark-f445c778b-bbkcd>Resource information>Node(raspberry)>Status(Running)>Ip(10.42.0.68)

minio_endpoint = "http://s3a-hl.data-platform:9000"  # Ensure this matches your setup
minio_access_key = "D7wE4fYTCf5D2FAPRIuO"
minio_secret_key = "7oDFMtaieNlvPec6K0SHFTpmYY9F7GRLSEQq2KxO"
minio_bucket = "test"

spark = SparkSession.builder \
    .appName("MinIOs") \
    .config('spark.master','spark://spark-master-svc:7077')\
    .config("spark.driver.host", "10.42.0.68")\
    .config("spark.driver.bindAddress", "10.42.0.68")\
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
    .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint) \
    .config("spark.hadoop.fs.s3a.access.key", minio_access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key) \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .getOrCreate()


dataframe = spark.read.json('s3a://test/orders.json')
average = dataframe.agg({'amount':'avg'})
average.write.format("csv").option("header", "true").save("s3a://test/json/")
average.show()

df = spark.read.csv("s3a://test/taxi.csv")
df.show()
spark.stop()
}

