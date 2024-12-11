import tensorflow as tf
from . import params
from .model import VGGModel
import os

current_dir = os.path.dirname(__file__)
best_model_weights = os.path.join(current_dir, '..', 'weights', 'my-weights.weights.h5')

def predict(img):
    model = VGGModel()
    model(tf.keras.Input(shape=(params.IMG_SIZE, params.IMG_SIZE, 3)))

    if not os.path.exists(best_model_weights):
        return (False, -1)

    model.load_weights(best_model_weights)

    img = img.convert("RGB")
    img = img.resize((params.IMG_SIZE, params.IMG_SIZE))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch of size 1
    img_array = img_array / 255.0  # Normalize the pixel values
    tensor_image = tf.convert_to_tensor(img_array)

    # Make predictions
    predictions = model.call(tensor_image)

    if predictions[0][0] > 0.5:
        return (True, predictions[0][0])
    else:
        return (False, predictions[0][0])

