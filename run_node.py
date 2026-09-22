import subprocess
import sys
import os

def run_node(script_name):
    node_path = "C:\\Program Files\\nodejs\\node.exe"
    if not os.path.exists(node_path):
        print(f"Error: node.exe not found at {node_path}")
        sys.exit(1)
        
    print(f"Running: {node_path} {script_name}...")
    result = subprocess.run([node_path, script_name], capture_output=True, text=True)
    
    print("\n--- STDOUT ---")
    print(result.stdout)
    
    print("--- STDERR ---")
    print(result.stderr)
    
    print(f"Exit code: {result.returncode}")
    sys.exit(result.returncode)

if __name__ == "__main__":
    script = sys.argv[1] if len(sys.argv) > 1 else "scratch_generate_fallbacks.js"
    run_node(script)
