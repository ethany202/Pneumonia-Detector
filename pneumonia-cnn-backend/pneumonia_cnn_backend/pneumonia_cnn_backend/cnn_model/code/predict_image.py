import tensorflow as tf
from . import params
from .model import VGGModel
import os
import matplotlib.pyplot as plt

current_dir = os.path.dirname(__file__)
best_model_weights = os.path.join(current_dir, '..', 'weights', 'my-weights.weights.h5')
# saliency_folder = '/kaggle/working/saliency_maps'

def predict(img, folder_location):
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

    generate_saliency_map(model, tensor_image, os.path.join(folder_location, "saliency_latest.jpeg"))

    if predictions[0][0] > 0.5:
        return (True, predictions[0][0])
    else:
        return (False, predictions[0][0])


def generate_saliency_map(model, tensor_image, output_path):
    """
    Generate a saliency map for a single image.

    Args:
        model: Trained TensorFlow model.
        image_path: Path to the input image.
        output_path: Path to save the saliency map.
    
    Returns:
        None. The saliency map is saved to the specified output path.
    """
    try:
        # Load and preprocess the image
        # img = Image.open(image_path).resize((224, 224))
        # img_array = np.array(img.convert('RGB')) / 255.0  # Normalize to [0, 1]
        # img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)
        # img_tensor = tf.expand_dims(img_tensor, axis=0)  # Add batch dimension

        # Compute the saliency map
        with tf.GradientTape() as tape:
            tape.watch(tensor_image)  # Ensure TensorFlow watches the input tensor
            predictions = model(tensor_image)
            class_idx = tf.argmax(predictions[0])  # Predicted class index
            class_score = predictions[0, class_idx]

        # Get gradients
        gradients = tape.gradient(class_score, tensor_image)
        saliency = tf.reduce_max(tf.abs(gradients), axis=-1)[0]  # Reduce batch & color channels
        
        # Normalize saliency map
        saliency = (saliency - tf.reduce_min(saliency)) / (tf.reduce_max(saliency) - tf.reduce_min(saliency))
        # Save the saliency map
        plt.imsave(output_path, saliency.numpy(), cmap='hot')
        print(f"Saliency map saved to: {output_path}")
    
    except Exception as e:
        print(f"Error generating saliency map: {e}")