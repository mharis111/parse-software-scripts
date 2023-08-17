import subprocess
import os
import sys

def execute_code(files):
# Iterate over the list of files
    for file in files:
        # Create a new virtual environment for each file
        venv_dir = f"./venv_{os.path.splitext(file)[0]}"  # Use the file name to create a unique venv directory
        subprocess.run([sys.executable, "-m", "venv", venv_dir])

        # Assume that the requirements.txt is in the same directory as the file
        requirements_file = os.path.join(os.path.dirname(file), "requirements.txt")

        # Install requirements if the requirements file exists
        if os.path.exists(requirements_file):
            subprocess.run([f"{venv_dir}/bin/pip", "install", "-r", requirements_file])

        # Check if the file is a Python script or a Jupyter notebook
        if file.endswith(".py"):
            # If it's a Python script, use the Python interpreter of the venv to execute it
            completed_process = subprocess.run([f"{venv_dir}/bin/python", file], capture_output=True, text=True)
            print(completed_process.stdout)
            print(completed_process.stderr)
        elif file.endswith(".ipynb"):
            # If it's a Jupyter notebook, use nbconvert to execute it
            completed_process = subprocess.run([f"{venv_dir}/bin/jupyter", "nbconvert", "--execute", "--inplace", file], capture_output=True, text=True)
            print(completed_process.stdout)
            print(completed_process.stderr)

    # remove the venv directory after running the file if no longer need it
     subprocess.run(["rm", "-rf", venv_dir])
