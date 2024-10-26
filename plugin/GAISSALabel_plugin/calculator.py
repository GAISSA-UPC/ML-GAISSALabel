import os, csv
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2_as_graph
import torch
from fvcore.nn import FlopCountAnalysis

def calculateH5(model_path, output_path):
    model = load_model(model_path)

    #### MODEL SIZE (# parameters)
    # Get number of parameters
    num_params = model.count_params()

    #### MODEL FILE SIZE
    model_size_bytes = os.path.getsize(model_path)
    model_size_mb = model_size_bytes / (1024 * 1024)

    #### FLOPS
    # convert tf.keras model into frozen graph to count FLOPS about operations used at inference
    # FLOPS depends on batch size
    inputs = [
        tf.TensorSpec([1] + (list(inp.shape[1:]) if not isinstance(inp.shape[1:], list) else inp.shape[1:]), inp.dtype)
        for inp in model.inputs
    ]
    real_model = tf.function(model).get_concrete_function(inputs)
    frozen_func, _ = convert_variables_to_constants_v2_as_graph(real_model)

    # Calculate FLOPS with tf.profiler
    run_meta = tf.compat.v1.RunMetadata()
    opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()
    flops = tf.compat.v1.profiler.profile(
        graph=frozen_func.graph, run_meta=run_meta, cmd="scope", options=opts
    )
    
    
    # Writing to CSV
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(['model_size', 'file_size', 'flops'])

        # Write the values
        writer.writerow([num_params, model_size_mb, flops.total_float_ops])

def calculatePyTorch(model_path, output_path, input_shape=None):
    model = torch.load(model_path)
    model.eval()

    #### MODEL SIZE (# parameters)
    num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

    #### MODEL FILE SIZE
    model_size_bytes = os.path.getsize(model_path)
    model_size_mb = model_size_bytes / (1024 * 1024)

    #### FLOPS for PyTorch model
    # Check if the user provided an input shape, otherwise default to (1, 3, 224, 224) for image models
    if input_shape is None:
        print("No input shape provided. Defaulting to image model input shape: (1, 3, 224, 224)")
        input_shape = (1, 3, 224, 224)

    try:
        # Create a dummy input tensor with the specified shape
        if len(input_shape) == 2:  # For language models, we assume input shape like (batch_size, sequence_length)
            input_tensor = torch.randint(0, 30522, input_shape, dtype=torch.long)
        else:
            input_tensor = torch.randn(input_shape)
        flops = FlopCountAnalysis(model, input_tensor).total()
    except Exception as e:
        print(f"Error calculating FLOPS: {e}")
        flops = "N/A"

    # Writing to CSV
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['model_size', 'file_size', 'flops'])
        writer.writerow([num_params, model_size_mb, flops])