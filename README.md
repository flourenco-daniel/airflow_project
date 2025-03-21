# airflow_project Documentation

## Introduction
This document outlines the setup and configuration of an Airflow project using Astro, along with additional components such as Spark, MinIO, and Metabase. The project is based on Mark Lamberti's course and includes various helpers, Spark integration, and a custom `docker-compose.override.yml` file.

## Setting Up Astro
Astro is the recommended way to create an Airflow environment. To get started, refer to the official documentation:
[Astro Documentation - First DAG CLI](https://www.astronomer.io/docs/astro/first-dag-cli)

## Docker-Compose Configuration
The `docker-compose.yml` file defines the necessary services and their configurations.

### Services

#### 1. **Airflow Components**
- **Webserver**: Runs the Airflow UI.
- **Scheduler**: Schedules and monitors DAG executions.
- **Triggerer**: Handles task triggers.

All these services are connected to the `ndsnet` network.

#### 2. **MinIO**
- **Image**: `minio/minio:RELEASE.2024-06-13T22-53-53Z`
- **Ports**:
  - `9000:9000` (Main MinIO service)
  - `9001:9001` (MinIO Console UI)
- **Environment Variables**:
  - `MINIO_ROOT_USER`: `minio`
  - `MINIO_ROOT_PASSWORD`: `minio123`
- **Healthcheck**: Monitors the MinIO service to ensure availability.

#### 3. **Spark Cluster**
- **Spark Master**:
  - **Image**: `airflow/spark-master`
  - **Ports**:
    - `8082:8080` (Spark Web UI)
    - `7077:7077` (Spark Master Node)
  - **Environment Variables**:
    - `INIT_DAEMON_STEP=setup_spark`

- **Spark Worker**:
  - **Image**: `airflow/spark-worker`
  - **Depends on**: Spark Master
  - **Ports**:
    - `8081:8081` (Spark Worker Web UI)
  - **Environment Variables**:
    - `SPARK_MASTER=spark://spark-master:7077`

#### 4. **Metabase**
- **Image**: `metabase/metabase:v0.52.8.4`
- **Ports**:
  - `3000:3000` (Metabase UI)
- **Volumes**:
  - `./include/data/metabase:/metabase-data` (Persistent storage for Metabase configurations)

#### 5. **Docker Proxy**
- **Image**: `alpine/socat`
- **Command**:
  - `"TCP4-LISTEN:2375,fork,reuseaddr UNIX-CONNECT:/var/run/docker.sock"`
- **Ports**:
  - `2376:2375` (Exposes the Docker socket to allow remote communication)

### Network Configuration
All services are connected to a custom Docker network:
```yaml
networks:
  ndsnet:
    driver: bridge
```
This ensures that all services can communicate securely within the same isolated network.

## Ensuring No Containers Are Running
Before starting the project, ensure that no containers are running by executing the following command:
```sh
astro dev stop
```
If you receive the error message:
```
Error: failed to execute cmd: exit status 1
```
it means that no containers are currently running.

## Building the Spark Images
Navigate to the `spark/master` directory and build the Spark Master image using the following command:
```sh
docker build -t airflow/spark-master .
```

Similarly, navigate to the `spark/worker` directory and build the Spark Worker image using:
```sh
docker build -t airflow/spark-worker .
```

## Starting the Project
Once all images are built, navigate to the root directory of the project and start the environment using:
```sh
astro dev start
```

## Summary
This setup provides a robust Airflow environment with:
- **Astro for Airflow orchestration**
- **MinIO for object storage**
- **Spark for big data processing**
- **Metabase for data visualization**
- **A Docker proxy for enhanced container communication**

