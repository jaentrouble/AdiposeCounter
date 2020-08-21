from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('tensorflow.python')

# hiddenimports = [
#     'tensorflow.python.ops.numpy_ops',
#     'tensorflow.python.keras.engine.base_layer_v1',
#     'tensorflow.python.eager.function'
# ]