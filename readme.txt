Dockers URL :- 
https://medium.com/@kayvan.sol2/pyspark-jupyter-notebooks-deployed-on-kubernetes-9141b33dbd3b
https://hub.docker.com/repositories/sonusukralia
http://127.0.0.1:8888/lab/workspaces/auto-i/tree/dc_jsmm.ipynb
http://localhost:8100/browser/test/json%2F
http://localhost:8081/

kubectl delete pod jupiter-spark-5467ff7cd7-xsgp6 -n data-platform --grace-period 0 --force
kubectl apply -f jupyter.yaml
{
apiVersion: apps/v1
kind: Deployment
metadata:
   name: jupiter-spark
   namespace: default
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
              image: docker.arvancloud.ir/jupyter/all-spark-notebook
              imagePullPolicy: IfNotPresent
              ports:
              - containerPort: 8888
              env: 
              - name: JUPYTER_ENABLE_LAB
                value: "yes"
---
apiVersion: v1
kind: Service
metadata:
   name: jupiter-spark-svc
   namespace: default
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
