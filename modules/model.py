import tensorflow as tf   
from tensorflow import keras
from tensorflow.keras import layers
from keras.layers import Dense, Conv2D, BatchNormalization, Activation, ZeroPadding2D
from keras.layers import AveragePooling2D, MaxPooling2D, Flatten, Add
from keras.models import Model
tf.get_logger().setLevel('INFO')

image_size = (256, 256)

def make_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)

    # Entry block
    x = layers.experimental.preprocessing.Rescaling(1.0 / 255)(inputs)
    x = Conv2D(32, kernel_size=(3, 3), strides=2, padding="same")(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    x = Conv2D(64, kernel_size=(3, 3), padding="same")(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [32, 64, 128, 256]:
        
        x = layers.SeparableConv2D(size, kernel_size=(3, 3), padding="same")(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        
        x = layers.SeparableConv2D(size, kernel_size=(3, 3), padding="same")(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        
        x = MaxPooling2D((3, 3), strides=2, padding="same")(x)

        # Project residual
        residual = Conv2D(size, kernel_size=(1, 1), strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(128, kernel_size=(3, 3), padding="same")(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)

def run_inference(model_path, image_path, image_size=image_size):
    model = make_model(input_shape=image_size + (3,), num_classes=2)
    model.compile(optimizer=keras.optimizers.Adam(1e-3),
                          loss="binary_crossentropy",
                          metrics=["accuracy"])
    model.load_weights(model_path)
    img = keras.preprocessing.image.load_img(image_path, target_size=image_size)
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    prediction = model.predict(img_array)
    score = prediction[0]
    return score
