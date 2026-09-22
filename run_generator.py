import subprocess
import os

node_path = "C:\\Program Files\\nodejs\\node.exe"
script_path = "scratch_generate_fallbacks.js"

print("Checking Node.js path...")
if not os.path.exists(node_path):
    print(f"Error: Node.js not found at {node_path}")
elif not os.path.exists(script_path):
    print(f"Error: Script not found at {script_path}")
else:
    print("Paths verified! Running fallback generator...")
    with open("generator_log.txt", "w") as log_file:
        result = subprocess.run(
            [node_path, script_path],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True
        )
        print(f"Finished. Exit code: {result.returncode}")
        print("Check generator_log.txt for details.")
