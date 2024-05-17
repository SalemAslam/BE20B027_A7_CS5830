import tensorflow as tf
import numpy as np


def predict_image(model, data_point):
  """
  Classifies an image using a pre-trained model.

  This function takes a pre-trained Keras model and a preprocessed image 
  as input. It feeds the image through the model to obtain predictions, 
  then identifies the class with the highest predicted probability.

  Args:
    model (tf.keras.Model): The trained model used for classification.
    image (np.ndarray): A preprocessed image compatible with the model's input.

  Returns:
    str: The predicted class label for the image.
  """

  predictions = model.predict(data_point)  # Wrap in a batch for prediction
  predicted_class = np.argmax(predictions, axis=1)[0]  # Find most likely class
  return str(predicted_class)  # Return the class label as a string


def format_image(image):
  """
  Resizes an image for compatibility with the model.

  This function takes a PIL image object and resizes it to the dimensions 
  expected by the model for prediction.

  Args:
    image (PIL.Image): A PIL image object.

  Returns:
    PIL.Image: The resized image suitable for model input.
  """
  image = image.resize((28, 28))
  # Flatten and normalize the image for model input
  flattened_image = np.array(image, dtype='float32').reshape(-1) / 255.0  # Flatten and normalize to 0-1 range
  flattened_image = flattened_image[None, :]  # Add a new axis for batch dimension

  return flattened_image  # Modify dimensions if needed for your model
