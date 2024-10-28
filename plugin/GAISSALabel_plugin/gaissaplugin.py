import os
from plugin_interface import PluginInterface
from calculator import calculateH5, calculateSavedModel, calculatePyTorch

class PlugIn(PluginInterface):
    def generate_output(self, model_path, output_directory, filename):
        # Create the full path for the output file
        output_path = os.path.join(output_directory, f"{filename}.csv")

        # Detect model type based on file extension or directory
        if model_path.endswith('.h5'):
            calculateH5(model_path, output_path)
        
        elif os.path.isdir(model_path):  # SavedModel format is a directory
            input_shape = self._get_input_shape("Enter the input shape (e.g.: 1,224,224,3), or press Enter to default: ")
            calculateSavedModel(model_path, output_path, input_shape)
        
        elif model_path.endswith(('.pt', '.pth')):
            input_shape = self._get_input_shape("Enter the input shape (e.g.: 1,3,224,224), or press Enter to default: ")
            calculatePyTorch(model_path, output_path, input_shape)
        
        else:
            raise ValueError("Unsupported model format. Please provide a .h5, .pt, .pth file or a SavedModel directory.")
        
        print(f"Output file '{filename}' generated in '{output_directory}'")

    def _get_input_shape(self, prompt):
        # Prompts the user to enter an input shape and converts it to a tuple or returns None if no input is provided.
        # Converts 'None' strings to actual None values for flexibility.
        
        input_shape_str = input(prompt)
        if not input_shape_str:
            return None
        return tuple(int(dim) if dim != "None" else None for dim in input_shape_str.split(','))
