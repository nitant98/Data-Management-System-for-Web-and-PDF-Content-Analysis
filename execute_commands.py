import os
import subprocess

def run_command(command, cwd=None):
    """
    Runs a command in the terminal and checks if it executed successfully.
    cwd is the current working directory to execute the command in.
    """
    try:
        # Ensure the cwd parameter is properly passed to subprocess.run
        result = subprocess.run(command, check=True, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
        print(f"Command '{command}' executed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}':\n{e.stderr}")
        exit(1)  # Exit the script if the command failed

def main():
    # Dynamically get the current script directory
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Define commands with relative paths
    commands = [
        ("pip install -r requirements.txt", None),
        ("python Webscrapper.py", None),
        ("python grobid_parsing.py", os.path.join(base_path, "grobid_step")),
        ("pytest pytests/", None),  # Assuming you want to run pytest at the base directory
        ("pip install -r requirements.txt", os.path.join(base_path, "snowflake_transfer")),
        ("python snowflake.py", os.path.join(base_path, "snowflake_transfer")),
       
    ]

    for command, cwd in commands:
        run_command(command, cwd=cwd)

if __name__ == "__main__":
    main()
