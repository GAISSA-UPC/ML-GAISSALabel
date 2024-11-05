# GAISSALabel Plug-in

We offer you a plug-in that runs on the terminal of your server. It will help you generate a file with the configuration parameters of your model. Specifically, it will provide the size of the model, the size of its file, and the FLOPS.


## Installation and Usage

1. Decompress the downloaded file.
2. Access your console and navigate to the decompressed folder.
3. Create a Python virtual environment using the command:
    ```sh
    python -m venv env
    ```
4. Activate the virtual environment:
    ```sh
    source env/bin/activate
    ```
5. Install the requirements:
    ```sh
    pip install -r requirements.txt
    ```
6. Run the script and follow the instructions of the plug-in:
    ```sh
    python main_script.py
    ```

## Updating the GAISSALabel Plug-in
If the GAISSALabel Plug-in is modified, ensure that the new version of the ZIP file is copied to the public folder of the frontend Vue project with the name "GAISSALabel_plugin.zip", so users can access the updated plug-in through the download link.
