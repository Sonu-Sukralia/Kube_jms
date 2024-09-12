https://blog.min.io/dremio-minio-kubernetes-analytics/

kubectl apply -f dremio_deployment.yaml
{
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dremio
  namespace: data-platform
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dremio
  template:
    metadata:
      labels:
        app: dremio
    spec:
      containers:
        - name: dremio
          image: dremio/dremio-oss:latest
          ports:
            - containerPort: 9047 # Dremio UI
            - containerPort: 31010 # ODBC/JDBC client connections
            - containerPort: 45678 # Internal Dremio communication
          env:
            - name: SERVICES_COORDINATOR_ENABLED
              value: "true"
            - name: SERVICES_EXECUTOR_ENABLED
              value: "true"
          volumeMounts:
            - name: dremio-data
              mountPath: /opt/dremio/data
      volumes:
        - name: dremio-data
          persistentVolumeClaim:
            claimName: dremio-pvc
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dremio-pvc
  namespace: data-platform
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi

}



Kubectl apply -f dremio_service.yaml
{
apiVersion: v1
kind: Service
metadata:
  name: dremio-service
  namespace: data-platform
spec:
  selector:
    app: dremio
  ports:
    - protocol: TCP
      port: 9047
      targetPort: 9047
      name: http
    - protocol: TCP
      port: 31010
      targetPort: 31010
      name: odbc-jdbc
    - protocol: TCP
      port: 45678
      targetPort: 45678
      name: internal
  type: LoadBalancer

}





