import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2_as_graph

model_path = '/Users/pduran/Desktop/TFG/deploy-GAISSA/models/model_fashion.h5'

model = load_model(model_path)
model.summary()

#### MODEL SIZE (# parameters)
# Get number of parameters
num_params = model.count_params()
print(f"Number of parameters: {num_params}")

#### MODEL FILE SIZE
model_size_bytes = os.path.getsize(model_path)
model_size_mb = model_size_bytes / (1024 * 1024)
print(f"Model size: {model_size_mb} MB")

#### FLOPS
# convert tf.keras model into frozen graph to count FLOPS about operations used at inference
# FLOPS depends on batch size
inputs = [
    tf.TensorSpec([1] + inp.shape[1:], inp.dtype) for inp in model.inputs
]
real_model = tf.function(model).get_concrete_function(inputs)
frozen_func, _ = convert_variables_to_constants_v2_as_graph(real_model)

# Calculate FLOPS with tf.profiler
run_meta = tf.compat.v1.RunMetadata()
opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()
flops = tf.compat.v1.profiler.profile(
    graph=frozen_func.graph, run_meta=run_meta, cmd="scope", options=opts
)

print(f"Total FLOPS: {flops.total_float_ops}")
