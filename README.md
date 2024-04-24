# ConnectionTracker app | docker compose and k8s

## Overview

Welcome to the ConnectionTracker application repository! This repository provides comprehensive configurations and setup instructions for deploying the ConnectionTracker application using both Docker Compose and Kubernetes (k8s) orchestration platforms.

ConnectionTracker is a versatile application designed to track and manage connections across various components of a system. It offers features such as monitoring, logging, and database management, making it a valuable tool for developers and system administrators alike.

In this repository, you'll find detailed guides and configuration files to deploy ConnectionTracker using Docker Compose for local development and testing environments. Additionally, we provide Kubernetes manifests for deploying ConnectionTracker in a production-ready Kubernetes cluster, ensuring scalability, resilience, and ease of management.

Whether you're a developer looking to set up a local development environment using Docker Compose or an operations engineer deploying a distributed application on Kubernetes, this repository has you covered. Follow the instructions below to get started with deploying ConnectionTracker in your preferred environment.

## Docker Compose

### Setup and Deployment

1. Navigate to the root directory of the project.
2. Run the following command to start the services:

```bash
cd ConnectionTracker
sudo docker compose up -d # if port 27017 is in use, run: sudo pkill mongod
sudo docker compose logs
```

### Access Services

- Web Application: [http://127.0.0.1:2000](http://127.0.0.1:2000)
- Backend Service: [http://127.0.0.1:7050](http://127.0.0.1:7050)
- PGAdmin Web Interface: [http://127.0.0.1:5050](http://127.0.0.1:5050) (Credentials: username: mustafakeser@zoho.com, password: 123456)
- Monitoring Web Interface: [http://127.0.0.1:9090](http://127.0.0.1:9090)
- Grafana Web Interface: [http://127.0.0.1:3000](http://127.0.0.1:3000) (Credentials: username: admin, password: 123456)

### Useful Commands

- Access PostgreSQL Docker Container:

```bash
docker exec -it postgres_postgres_1 sh
psql -U postgres -d postgres
\l
\dt
SELECT * FROM public.actor LIMIT 3;
```

- Log a Service:

```bash
docker-compose logs webapp
```

- Reset Grafana Password:

```bash
docker exec -it postgres_logging_1 sh
grafana-cli --homepath "/usr/share/grafana" admin reset-admin-password 123456
```

- Access MongoDB Container:

```bash
docker exec -it postgres_mongodb_1 sh
mongosh -u root -p password

use mydatabase
db.createCollection("mycollection")
db.mycollection.insertMany([
   {
       "name": "Alice",
       "age": 25,
       "city": "Los Angeles"
   },
   {
       "name": "Bob",
       "age": 35,
       "city": "Chicago"
   },
   {
       "name": "Emily",
       "age": 28,
       "city": "San Francisco"
   }
])
db.mycollection.find().pretty()
```

## Kubernetes

### Installation Steps

1. Install Microk8s:

```bash
sudo apt install snapd
sudo snap install microk8s --channel=1.29/stable --classic
sudo microk8s status --wait-ready
sudo usermod -a -G microk8s desktop
sudo chown -f -R desktop ~/.kube

# Enable kubectl autocompletion
kubectl='microk8s kubectl'
source <(kubectl completion bash)

# Enable required addons
microk8s enable dns storage dashboard storage ingress
microk8s enable metallb:10.64.140.43-10.64.140.49
```

2. Verify Installation:

```bash
kubectl get pods --all-namespaces 
```

### Deployments

1. Convert Docker Compose to Kubernetes manifests:

```bash
mkdir k8s
# Install Kompose: [https://kompose.io/installation/](https://kompose.io/installation/)
kompose convert -o ./k8s/
cd k8s
```
Some changes applied to automatically created kompose files
* Changed monitoring-deployment.yaml's volume name and configmap name.
* Added type: LoadBalancer web-interface services.
* Created prometheus_configmap.yaml manually.

2. Apply Kubernetes Resources:

```bash
cd k8s
kubectl create namespace connection-tracker
kubectl apply -f backend-deployment.yaml -n connection-tracker
kubectl apply -f webapp-deployment.yaml -n connection-tracker
kubectl apply -f mongodb-deployment.yaml -n connection-tracker
kubectl apply -f pgadmin-service.yaml -n connection-tracker
kubectl apply -f backend-service.yaml -n connection-tracker
kubectl apply -f mongodb-service.yaml -n connection-tracker
kubectl apply -f postgres-data-persistentvolumeclaim.yaml -n connection-tracker
kubectl apply -f grafana-data-persistentvolumeclaim.yaml -n connection-tracker
kubectl apply -f monitoring-claim0-persistentvolumeclaim.yaml -n connection-tracker
kubectl apply -f postgres-deployment.yaml -n connection-tracker
kubectl apply -f logging-deployment.yaml -n connection-tracker
kubectl apply -f monitoring-deployment.yaml -n connection-tracker
kubectl apply -f logging-service.yaml -n connection-tracker
kubectl apply -f monitoring-service.yaml -n connection-tracker
kubectl apply -f webapp-service.yaml -n connection-tracker
kubectl apply -f mongodb-data-persistentvolumeclaim.yaml -n connection-tracker
kubectl apply -f pgadmin-deployment.yaml -n connection-tracker
kubectl apply -f prometheus_configmap.yaml -n connection-tracker
kubectl apply -f postgres-service.yaml -n connection-tracker
```

### Checking Status and Accessing Services

1. Check Pods Status:

```bash
kubectl get pods -n connection-tracker -w
```

2. Access Services:

Use external ip adresses and ports to access services.

```bash
kubectl get service -n connection-tracker
```

3. Access Kubernetes Dashboard:

```bash
microk8s dashboard-proxy # Use URL and token from the terminal.
```

4. Note: Use cluster IP addresses for Grafana and PostgreSQL connections corresponding to each service. You can check addresses with:

```bash
kubectl get service -n connection-tracker
```

5. pgadmin web-interface settings.
```bash
General Name: postgres
Connection Host name/adress: 10.152.183.133 #your postgress service cluster ip
Connection Maintaince database: postgres
Connection Username: postgres
Connection Password: 123456
```
6. grafana connections settings.

```bash
grafana username: admin, password: 123456
#postgres connection
Host URL: 10.152.183.133:5432 #your postgress service clusterip:5432
Database name: postgres
Username: postgres
Password: 123456
TLS/SSL Mode: disable
Save & Test

#prometheus connection
Prometheus server URL: 10.152.183.78:9090  #your monitoring service clusterip:9090 or externalip:9090
Save & Test
```
### Result

<iframe src="Kubernetes-Dashboard.pdf" width="100%" height="500" frameborder="0">

<object data="Kubernetes-Dashboard.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="Kubernetes-Dashboard.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="Kubernetes-Dashboard.pdf">Download PDF</a>.</p>
    </embed>
</object>

## Note

Make sure to adjust configurations and credentials according to your environment.
