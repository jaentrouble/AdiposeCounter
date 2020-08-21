import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras
import json
from .weights import w
import numpy as np



def full_conv4_2(inputs):
    x = layers.Conv2D(32, 3, padding='same', activation='relu')(inputs)
    x = layers.Conv2D(32, 3, padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64, 3, padding='same', activation='relu')(x)
    x = layers.Conv2D(64, 3, padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Conv2D(1, 3, padding='same', activation='linear')(x)
    x = tf.squeeze(x, axis=-1)
    outputs = layers.Activation('linear', dtype='float32')(x)
    return outputs

class AdiposeModel(keras.Model):
    def __init__(self, inputs, model_function):
        """
        Because of numerical stability, softmax layer should be
        taken out, and use it only when not training.
        Args
            inputs : keras.Input
            model_function : function that takes keras.Input and returns
            output tensor of logits
        """
        super().__init__()
        outputs = model_function(inputs)
        self.logits = keras.Model(inputs=inputs, outputs=outputs)
        self.logits.summary()
        
    def call(self, inputs, training=None):
        if training:
            return self.logits(inputs, training=training)
        return tf.math.sigmoid(self.logits(inputs, training=training))

def get_model():
    """
    return a model with loaded weights
    """
    model = AdiposeModel(keras.Input((200,200,3)), full_conv4_2)
    weights = json.loads(w)
    converted_weights = []
    for weight in weights:
        converted_weights.append(np.array(weight,dtype=np.float32))
    model.set_weights(converted_weights)
    return model

if __name__ == '__main__':
    mymodel = get_model()