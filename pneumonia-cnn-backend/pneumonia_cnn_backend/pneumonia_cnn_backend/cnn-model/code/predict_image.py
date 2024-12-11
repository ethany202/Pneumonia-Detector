import tensorflow as tf
import params
import VGGModel
import os

best_model_weights = '../weights/my-weights.weights.h5'

def predict(img):
    model = VGGModel()
    model(tf.keras.Input(shape=(params.IMG_SIZE, params.IMG_SIZE, 3)))
    model.load_weights(best_model_weights)

    if not os.path.exists(best_model_weights):
        return False

    img = img.resize((params.IMG_SIZE, params.IMG_SIZE))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch of size 1
    img_array = img_array / 255.0  # Normalize the pixel values

    # Make predictions
    predictions = model.call(img_array)

    print(predictions[0][0])

    if predictions[0][0] > 0.5:
        return True
    else:
        return False
