import os
import shutil

# Define the filename of the file you want to move
source_filename = 'dag_run.py'

# Define the relative path to the destination directory
# For example, 'destination_directory' relative to the current working directory
destination_directory = 'airflow-dbt-cloud/dags/'

# Construct the full source path (optional if you are in the same directory)
source_path = os.path.join(os.getcwd(), source_filename)

# Construct the full destination path
destination_path = os.path.join(os.getcwd(), destination_directory, source_filename)

# Move the file
shutil.move(source_path, destination_path)

print(f"Moved '{source_filename}' to '{destination_path}'")
