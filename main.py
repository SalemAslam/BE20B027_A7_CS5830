import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from io import BytesIO
from PIL import Image
import numpy as np
import uvicorn  # Server on which FastAPI runs : "uvicorn main:app --reload" on terminal to view the web interface of FastAPI
import time
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Gauge
import psutil

# Importing helper functions
from load_model import load_model
from predict_format_image import predict_image, format_image

# Create the FastAPI application
app = FastAPI(title="Digit Recognition API (BE20B027)")

# Load the pre-trained MNIST model
model_path = "/Users/Salem Aslam/Documents/3. Academics/#Sem8/Lab/A6/MNIST_model.h5"
model = load_model(model_path)
# Set the model to inference mode for prediction
model.trainable = False

# Prometheus metrics
request_counter = Counter("Client_IP_count", "Total number of API requests", ["client_ip"])
run_time = Gauge("API_runtime", "Time taken for inference in seconds")
processing_time_per_char_gauge = Gauge("processing_time_per_char_microseconds", "Processing time per character in microseconds")

network_receive_bytes = Gauge("network_receive_bytes", "Total network receive bytes")
network_transmit_bytes = Gauge("network_transmit_bytes", "Total network transmit bytes")

memory_utilization = Gauge("API_memory_utilization", "API memory utilization in percent")
cpu_utilization = Gauge("API_cpu_utilization", "API CPU utilization in percent")

# This line registers the metrics with a Prometheus instrumentation library
# and exposes them for scraping by a Prometheus server.
Instrumentator().instrument(app).expose(app)


@app.post('/predict')
async def predict(request: Request, uploaded_image: UploadFile = File(...)):
    """
    Predicts the digit present in an uploaded image.

    This endpoint accepts an image file as input and performs digit classification using 
    the pre-trained MNIST model. It first validates the image format (JPEG, JPG, or PNG), 
    then preprocesses the image by converting it to grayscale and resizing it to the model's 
    expected dimensions. Finally, the image is flattened and normalized before feeding it 
    to the model for prediction. The predicted digit label is returned in the response.

    Raises:
        HTTPException: If the uploaded file format is not supported.
    """

    # Read the image content from the uploaded file
    image_content = await uploaded_image.read()

    # Define accepted image formats
    accepted_formats = ['.jpeg', '.jpg', '.png']
    file_extension = os.path.splitext(uploaded_image.filename)[1].lower()

    # Validate image format
    if file_extension not in accepted_formats:
        raise HTTPException(status_code=400, detail="Bad file format. Accepted formats are .jpeg, .jpg, .png")

    client_ip = request.client.host
    request_counter.labels(client_ip=client_ip).inc()

    # Extract filename without extension
    filename = os.path.splitext(uploaded_image.filename)[0]

    # Open the image from the byte stream
    image = Image.open(BytesIO(image_content))

    # Convert the image to grayscale
    grayscale_image = image.convert('L')

    # Preprocess the image using the helper function
    preprocessed_image = format_image(grayscale_image)

    start_time = time.time()

    # Predict the digit using the loaded model and helper function
    digit = predict_image(model, preprocessed_image)
    
    end_time = time.time()
    inference_time = end_time - start_time
    run_time.set(inference_time)

    # Calculate the effective processing time per character
    input_length = len(image_content)  # Use the length of the file contents
    processing_time_per_char = (inference_time * 1e6) / input_length  # Convert to microseconds per character
    processing_time_per_char_gauge.set(processing_time_per_char)

    # Get network I/O bytes
    net_io = psutil.net_io_counters()
    network_receive_bytes.set(net_io.bytes_recv)
    network_transmit_bytes.set(net_io.bytes_sent)

    # Return the predicted digit in the response
    return {"digit": digit}

