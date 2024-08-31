1. docker pull sonusukralia/miniod:3.5
2. docker run --hostname minio -d --name minio -p 8099:9000 -p 8100:9001 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=minio123 --network new_spark-network sonusukralia/miniod:3.5

pi@raspberry:~/minio_yaml $ docker images
REPOSITORY                                        TAG       IMAGE ID       CREATED         SIZE
sonusukralia/sparkd                               3.5       53ec21ac8e6e   5 days ago      1.73GB
sonusukralia/jupyterd                             3.5       66a4718cc714   5 days ago      6.7GB
sonusukralia/miniod                               3.5       01c2ce3726af   5 days ago      291MB
pi@raspberry:~/minio_yaml $ docker ps
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS                      PORTS                                                                                  NAMES
7a76142e9b74   sonusukralia/miniod:3.5     "/opt/bitnami/script…"   36 minutes ago   Up 36 minutes               0.0.0.0:8099->9000/tcp, :::8099->9000/tcp, 0.0.0.0:8100->9001/tcp, :::8100->9001/tcp   minio
3d2085d38215   sonusukralia/jupyterd:3.5   "tini -g -- start-no…"   49 minutes ago   Up 49 minutes (unhealthy)   4040/tcp, 0.0.0.0:8888->8888/tcp, :::8888->8888/tcp                                    jupyter
629cb4d91dbe   sonusukralia/sparkd:3.5     "/opt/bitnami/script…"   49 minutes ago   Up 49 minutes               7077/tcp, 8080/tcp                                                                     new_spark-worker_2
2d1a00984e34   sonusukralia/sparkd:3.5     "/opt/bitnami/script…"   49 minutes ago   Up 49 minutes               7077/tcp, 8080/tcp                                                                     new_spark-worker_1
261183058cc2   sonusukralia/sparkd:3.5     "/opt/bitnami/script…"   49 minutes ago   Up 49 minutes               127.0.0.1:7077->7077/tcp, 127.0.0.1:8081->8080/tcp                                     spark
pi@raspberry:~/minio_yaml $ docker network ls
NETWORK ID     NAME                DRIVER    SCOPE
90d7ed77d3f3   bridge              bridge    local
01cc9bc83b08   host                host      local
a236812704b6   new_spark-network   bridge    local
75ca9754ed39   none                null      local
pi@raspberry:~/minio_yaml $ 
To access Minio :- 
docker run --hostname minio -d --name minio -p 8099:9000 -p 8100:9001 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=minio123 --network new_spark-network sonusukralia/miniod:3.5
Access Url :- http://localhost:8100
To access bucket server : http://minio:8100
docker exec -it minio bash
 -- I have no name!@minio:/opt/bitnami/minio-client$ cat /etc/hosts

Notes :- 
To check the networks
{
docker pull sonusukralia/miniod:3.5
docker run sonusukralia/miniod:3.5
docker run --hostname minio sonusukralia/miniod:3.5
docker network ls
docker network inspect minio_spark-network
docker run --hostname minio --network minio_spark_network bitnami/minio
docker run --hostname minio -d  --network minio_spark-network bitnami/minio
dockeer ps -a
docker stop jolly_blackwell
docker run --hostname minio -d --name minio  --network minio_spark-network bitnami/minio
docker stop minio
docker run --hostname minio -d --name minio  --network minio_spark-network bitnami/minio
docker rm minio
docker run --hostname minio -d --name minio -p 8099:9000 -p 8100:9001  --network minio_spark-network bitnami/minio
docker logs minio


docker run --hostname minio -d --name minio -p 8099:9000 -p 8100:9001 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=minio123 --network minio_spark-network bitnami/minio
Access Url :- http://localhost:8100

docker exec -it minio bash
 -- I have no name!@minio:/opt/bitnami/minio-client$ cat /etc/hosts
}





bitnami/minio                                     latest    60edf986514c   42 hours ago    291MB
docker.arvancloud.ir/bitnami/spark                3.5.0     de9ced01ed7b   6 months ago    1.73GB
docker.arvancloud.ir/jupyter/all-spark-notebook   latest    4dec64d08d4e   10 months ago   5.45GB
