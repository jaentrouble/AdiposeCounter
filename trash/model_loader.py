import tensorflow as tf
from tensorflow import keras
from .tf_models import adipose_models
import json
from .weights import w
import numpy as np

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


def get_model_from_saved_weights(model_f_name):
    model = AdiposeModel(keras.Input((200,200,3)), 
                    getattr(adipose_models, model_f_name))
    weight_dir = f'sources/tf_models/saved_models/{model_f_name}/1'
    model.load_weights(weight_dir)
    print('weights loaded')
    return model

def get_model(model_f_name):
    """
    return a model with loaded weights
    """
    model = AdiposeModel(keras.Input((200,200,3)), 
                    getattr(adipose_models, model_f_name))
    weights = json.loads(w)
    converted_weights = []
    for weight in weights:
        converted_weights.append(np.array(weight,dtype=np.float32))
    model.set_weights(converted_weights)
    return model

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    model = get_model('hr_5_3_0')
    with np.load('cell_mask_data.npz') as data:
        X = data['img']
        Y = data['mask']
    predict = model(X[:6])

    fig = plt.figure(figsize=(15,15))
    i = 1
    for img, pred in zip(X[:6], predict[:6]):
        ax = fig.add_subplot(6,2,i)
        ax.imshow(img)
        ax = fig.add_subplot(6,2,i+1)
        ax.imshow(pred)
        i += 2
    plt.show()