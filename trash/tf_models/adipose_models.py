import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import layers
from . import custom_layers as clayers

# Get inputs and return outputs
# Don't forget to squeeze output


def hr_5_3_0(inputs):
    x = [inputs]
    x = clayers.HighResolutionModule(
        filters=[8],
        blocks=[3],
        name='HR_0'
    )(x)
    x = clayers.HighResolutionModule(
        filters=[8,16],
        blocks=[3,3],
        name='HR_1'
    )(x)
    x = clayers.HighResolutionModule(
        filters=[8,16,32],
        blocks=[3,3,3],
        name='HR_2'
    )(x)
    x = clayers.HighResolutionModule(
        filters=[8,16,32,64],
        blocks=[3,3,3,3],
        name='HR_3'
    )(x)
    x = clayers.HighResolutionModule(
        filters=[8,16,32,64],
        blocks=[3,3,3,3],
        name='HR_4'
    )(x)
    x = clayers.HighResolutionFusion(
        filters=[8],
        name='Fusion_0'
    )(x)
    x = layers.Conv2D(
        1,
        1,
        padding='same',
        name='Final_conv'
    )(x[0])
    x = tf.squeeze(x, axis=-1)
    outputs = layers.Activation('linear', dtype='float32')(x)
    return outputs
