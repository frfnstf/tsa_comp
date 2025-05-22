import tensorflow as tf
from tensorflow import keras, data
import numpy as np
import kerastuner as kt
import os
from keras.models import Sequential
from keras import layers
from keras.layers import BatchNormalization, Conv2D, MaxPooling2D
from keras.layers import Activation, Flatten, Dropout, Dense
import time

# This class allows the program to update the displayed listbox according to the callbacks given by the model
class TrainingUpdateCallback(keras.callbacks.Callback):
    def __init__(self, update_func):
        super().__init__()
        self.update_func = update_func

    def on_epoch_begin(self, epoch, logs=None):
        self.update_func(f"Starting Epoch {epoch + 1}...")
        self.start_time = time.time()

    def on_epoch_end(self, epoch, logs=None):
        end_time = time.time()
        epoch_time = end_time - self.start_time
        self.update_func(f"Epoch {epoch + 1} ({epoch_time:.2f} s)")


# Function to train a TensorFlow model and predict crop disease
def classify_image(crop, filepath, update_func):

    """
        Utilizes the dedicated graphics card on the computer we will use for the competition
        This allows the model to train and predict at a faster speed, but the program can still function without it
        try-except is included to account for if this program is run on a device that doesn't have this hardware
    """
    try:
        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    except:
        pass

    image_size = (128, 128)
    batch_size = 64
    
    # Open up training dataset for the specific crop given by the user
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        f"Image_Datasets/{crop}",
        validation_split = 0.2,
        subset = "training",
        seed = 1337,
        image_size = image_size,
        batch_size = batch_size,
    )
    
    # Some images from the dataset are used for validation
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    f"Image_Datasets/{crop}",
        validation_split = 0.2,
        subset = "validation",
        seed = 1337,
        image_size = image_size,
        batch_size = batch_size,
    )

    # Incorporating some amount of data augmentation allows for the size of our dataset to be increased
    data_augmentation = keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.1)
        ]
    )

    inputs = keras.Input(shape=image_size + (3,))
    x = data_augmentation(inputs)
    x = layers.Rescaling(1./255)(x)

    train_ds = train_ds.map(
        lambda img, label: (data_augmentation(img), label),
        num_parallel_calls = data.AUTOTUNE
    )

    # Create a model that utilizes the pre-loaded data from keras tuner to enhance performance
    def create_model(hp):
        model = Sequential()

        input_shape = image_size + (3,)
        hp_units = hp.Int('units', min_value=128, max_value=1024, step=32)
        model

        num_classes = len(os.listdir(f"Image_Datasets/{crop}"))
        activation = 'softmax'

        model.add(Conv2D(32, (3, 3), padding='same', input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(BatchNormalization(axis=-1))
        model.add(MaxPooling2D(pool_size=(3,3)))
        model.add(Dropout(0.25))
        model.add(Conv2D(64, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization(axis=-1))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, (3, 3), padding='same'))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=-1))
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=-1))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(hp_units))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))
        model.add(Dense(num_classes))
        model.add(Activation(activation))

        hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=hp_learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

    # This is the number of times the program will do one complete pass of the entire training dataset
    epochs = 15

    # Check if a model exists, and load it if it does
    model_file = f"saved_models/{crop}_model.keras"

    # Note: when the finalized app is run, the program would use a saved model    
    if os.path.exists(model_file):
        update_func("Loading Model...")
        model = keras.models.load_model(model_file)

    # This part was only used during the training/creation of all of the pre-saved models
    else:
        update_func("Training New Model...")
        # Utilizing keras tuner
        tuner = kt.Hyperband(
            create_model,
            objective='val_accuracy',
            max_epochs=10,
            factor=3,
            directory='Tuner_Data',
            project_name=crop
        )

        tuner.search(
            train_ds,
            epochs=epochs,
            validation_data=val_ds,
            callbacks=[tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=0,
                restore_best_weights=True
            )]
        )
        
        # Using keras tuner allows you to get the optimal parameters for each model
        best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

        update_func(f"Optimal Number of Units: {best_hps.get('units')}")
        update_func(f"Optimal Learning Rate: {best_hps.get('learning_rate')}")
        update_func("")

        model = tuner.hypermodel.build(best_hps)
        update_callback = TrainingUpdateCallback(update_func)
        
        # Here, callbacks is what allows the listbox in the GUI to update periodically
        history = model.fit(train_ds, epochs=epochs, validation_data=val_ds, callbacks=[update_callback])

        update_func("")
        update_func("Model Training Complete!")

        # Save the trained model for future use
        os.makedirs("saved_models", exist_ok=True)
        model.save(model_file)
        update_func(f"Model Saved as {model_file}")

    # Given the image uploaded by the user, predict the crop disease, returning this along with the percent confidence
    img = keras.utils.load_img(filepath)
    img = keras.utils.img_to_array(img)
    img = tf.keras.preprocessing.image.smart_resize(img, (128, 128))
    img = tf.reshape(img, (-1, 128, 128, 3))

    update_func("Predicting Crop Disease...")

    prediction = model.predict(img)

    predicted_disease = sorted(os.listdir(f"Image_Datasets/{crop}"))[np.argmax(prediction)]
    percent_conf = str(round(100 * np.max(prediction), 2)) + "%"

    update_func("Prediction Complete.")
    update_func("")

    return predicted_disease, percent_conf
