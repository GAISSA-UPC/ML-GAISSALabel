from gaissaplugin import PlugIn
import os

def main():

    # Get user input for model path and output directory and filename
    model_path = input("Enter the model's file path: ")

    default_output_directory = "./plugin_output"
    output_directory = input(f"Enter the output directory (or continue to default: {default_output_directory}): ") or default_output_directory

    model_name = os.path.splitext(os.path.basename(model_path))[0]
    default_filename = f"{model_name}_output"
    filename = input(f"Enter the filename (or continue to default: {default_filename}): ") or default_filename

    # Instantiate the plugin
    plugin = PlugIn()

    # Call the plugin to generate the output
    plugin.generate_output(model_path, output_directory, filename)

if __name__ == "__main__":
    main()
