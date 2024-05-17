import requests
import time
import random
from multiprocessing import Pool

# Function to call the FastAPI endpoint with an image
def call_api(instance_url):
    """
    This function sends a POST request to the specified FastAPI instance URL 
    with an image for digit recognition.

    Args:
        instance_url (str): The URL of the FastAPI instance (e.g., "http://localhost:8000").

    Returns:
        None
    """

    image_path = "/Users/Salem Aslam/Documents/3. Academics/#Sem8/Lab/A6/digits_mnist_paint/mnist/0.png"
    # Ensure this path is correct and points to a valid image file

    with open(image_path, 'rb') as f:
        response = requests.post(f"http://{instance_url}/predict", files={"uploaded_image": f})

    print(f"Response from {instance_url}: {response.json()}")

# Function to continuously call the API from a worker process
def worker(instance_urls):
    """
    This function runs in a separate worker process and continuously calls the 
    call_api function for a randomly chosen URL from the provided list.

    Args:
        instance_urls (list): A list of FastAPI instance URLs.
    """

    while True:
        instance_url = random.choice(instance_urls)
        try:
            call_api(instance_url)
        except Exception as e:
            print(f"Error calling {instance_url}: {e}")
        time.sleep(1)  # Adjust the sleep time to control the load between calls

if __name__ == "__main__":
    """
    Main program execution block.
    """

    instance_urls = ["localhost:8000", "localhost:8001"] 
    pool = Pool(len(instance_urls))

    # Run worker functions in parallel using a process pool
    pool.map(worker, [instance_urls]*len(instance_urls))
