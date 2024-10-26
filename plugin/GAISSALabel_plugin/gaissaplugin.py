import os
from plugin_interface import PluginInterface
from calculator import calculateH5, calculatePyTorch

class PlugIn(PluginInterface):
    def generate_output(self, model_path, output_directory, filename):
        # Create the full path for the output file
        output_path = os.path.join(output_directory, filename + '.csv')

        # Detect model type based on file extension or directory
        if model_path.endswith('.h5'):
            calculateH5(model_path, output_path)
        elif model_path.endswith('.pt') or model_path.endswith('.pth'):
            # Ask the user if it's not an image model and they need to provide the input shape
            input_shape_str = input("Enter the input shape (e.g.: 1,3,224,224), or press Enter to default: ")
            if input_shape_str:
                input_shape = tuple(map(int, input_shape_str.split(',')))
            else:
                input_shape = None
            calculatePyTorch(model_path, output_path, input_shape)
        else:
            raise ValueError("Unsupported model format. Please provide a .h5, .pt, .pth file or a SavedModel directory.")

        print(f"Output file '{filename}' generated in '{output_directory}'")
