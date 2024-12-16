import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
from . import params
from .model import VGGModel
import os

current_dir = os.path.dirname(__file__)

# Define paths to training and validation directories
train_dir = os.path.join(current_dir, '..', 'data', 'train')
val_dir = os.path.join(current_dir, '..', 'data', 'val')

weights_path = os.path.join(current_dir, '..', 'weights', 'vgg16_imagenet.h5')
best_weights_path = os.path.join(current_dir, '..', 'weights', 'my-weights.weights.h5')

####
# NOTE: OUR MODEL WAS TRAINED IN KAGGLE NOTEBOOKS, HOWEVER, WE DECIDED TO PUT THE CODE HERE 
#       TO SHOW THE ARCHITECTURE AND PRE-PROCESSING DONE
####
def load_datasets():
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        batch_size=params.BATCH_SIZE,
        image_size=(params.IMG_SIZE, params.IMG_SIZE)
    )

    val_dataset = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        batch_size=params.BATCH_SIZE,
        image_size=(params.IMG_SIZE, params.IMG_SIZE)
    )

    return train_dataset, val_dataset


def train():
    model = VGGModel()

    model(tf.keras.Input(shape=(params.IMG_SIZE, params.IMG_SIZE, 3)))
    model.vgg16.load_weights(weights_path)

    print(model.head.summary())

    train_dataset, val_dataset = load_datasets()

    normalization_layer = tf.keras.layers.Rescaling(1./255)
    train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))
    val_dataset = val_dataset.map(lambda x, y: (normalization_layer(x), y))

    # Adding Data augmentation
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomRotation(0.1),
        tf.keras.layers.RandomZoom(0.1),
    ])

    # Preprocessing
    train_dataset = train_dataset.map(lambda x, y: (data_augmentation(x), y))

    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=weights_path, 
        save_weights_only=True,
        save_best_only=True,
        monitor='val_accuracy',
        mode='max',
        verbose=1
    )

    model.compile(
        optimizer=model.optimizer,
        loss=model.loss_fn,
        metrics=['accuracy', tf.keras.metrics.AUC()]
    )

    history = model.fit(
        x=train_dataset,
        validation_data=val_dataset,
        epochs=params.EPOCH_SIZE,
        callbacks=[cp_callback]
    )

def main():
    train()

if __name__ == '__main__':
    main()
