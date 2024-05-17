from tensorflow import keras


def load_model(path: str) -> keras.Model:
  """
  Loads a pre-trained Keras model from a specified file path.

  This function takes a string representing the file path to a saved 
  Keras model and loads it.

  Args:
      path (str): The file path to the saved Keras model.

  Returns:
      keras.Model: The loaded Keras model, or raises an exception if loading fails.
  """

  model = keras.models.load_model(path)
  return model
