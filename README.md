# Monitoring of FastAPI Application with Prometheus and Grafana for MNIST Digit Prediction and Dockerizing it

## Introduction
This project enhances a FastAPI application for MNIST digit recognition by integrating monitoring capabilities using Prometheus and Grafana. The application is containerized using Docker, enabling easy deployment and scaling across multiple instances. Monitoring includes tracking API usage, performance metrics, and resource utilization. This repository documents the steps taken to integrate these monitoring tools, dockerize the application, and perform load testing on the deployed instances.

## Setup Instructions

### Prerequisites
- Python 3.10.4
- Docker and Docker Compose
- Prometheus and Grafana

- ## Directory Structure
```
.
├── .dockerignore
├── Build a FastAPI for MNIST digit prediction.pdf
├── data/
├── digits_mnist_paint/
├── docker-compose.yml
├── Dockerfile
├── env/
├── load_model.py
├── load_test.py
├── main.py
├── mnist_model.h5
├── predict_format_image.py
├── prometheus.exe
├── prometheus.yml
├── requirement.txt
├── screenshots/
├── train_save_model.py
└── __pycache__/
```

### Installation
1. **Clone the repository:**
    ```bash
    git clone <repository-link>
    cd <repository-directory>
    ```

2. **Set up a virtual environment and install dependencies:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    pip install -r requirement.txt
    ```

3. **Build and run Docker containers:**
    ```bash
    docker-compose up --build
    ```

## FastAPI Application
The FastAPI application predicts digits from uploaded images using a pre-trained MNIST model. The `/predict` endpoint accepts image files, preprocesses them, and returns the predicted digit.

## Prometheus Integration
Prometheus collects metrics from the FastAPI application. Key metrics include:
- `api_requests_total`: Total number of API requests, tracked by client IP.
- `api_inference_time_seconds`: Time taken for inference in seconds.
- `api_processing_time_per_char_microseconds`: Processing time per character in microseconds.
- `api_network_receive_bytes`: Total network receive bytes.
- `api_network_transmit_bytes`: Total network transmit bytes.
- `api_memory_utilization_percent`: Memory utilization of the API.
- `api_cpu_utilization_percent`: CPU utilization of the API.

Metrics are exposed at the `/metrics` endpoint.

## Grafana Integration
Grafana dashboards visualize metrics collected by Prometheus, including:
- API processing time per character (T/L).
- Total API requests.
- API requests created.
- API run time.

These dashboards provide real-time insights into the application’s performance and resource utilization.

## Load Testing
A Python script (`load_test.py`) continuously calls the `/predict` endpoint using random images from a specified folder. This simulates concurrent users and generates a realistic load on the application. The script uses multiple processes to increase the load, targeting the API endpoints of both instances.

## Results
The Grafana dashboard showcases performance metrics for two instances of the FastAPI application. Key observations include:
- High initial processing time per character, stabilizing to 30,000-40,000 microseconds.
- Consistently low API run time (0.03 to 0.04 seconds).
- Steady memory utilization at 29.4% and 29.6%.
- Gradual increase in network received bytes, reaching up to 4,000,000 bytes.
- CPU utilization around 5%.
- One instance connected 77 times, and another 33 times.

## Conclusion
Integrating Prometheus and Grafana with the FastAPI application provided a robust monitoring solution. Dockerization facilitated easy deployment and scaling, while continuous load testing ensured system reliability and performance. The project successfully demonstrated the effectiveness of using these tools for monitoring and managing a microservices architecture.


## Author
Salem Aslam (BE20B027)
