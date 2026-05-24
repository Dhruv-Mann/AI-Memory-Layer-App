import os
import subprocess
import sys

def build():
    print("Starting PyInstaller packaging for FastAPI sidecar...")
    
    # We build main.py from the app folder
    # We will output the compiled sidecar into the sidecar/dist/ directory
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name=app",
        "--onefile",
        "--console",
        "app/main.py"
    ]
    
    # Hidden imports required by dynamic library loadings
    hidden_imports = [
        "uvicorn",
        "fastapi",
        "pydantic",
        "lancedb",
        "pyarrow",
        "pypdf",
        "sentence_transformers",
        "transformers",
        "tokenizers",
        "onnxruntime",
        "requests",
        "keyring",
        "pysqlcipher3"
    ]
    
    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])
        
    print(f"Running command: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd="sidecar")
    print("PyInstaller build finished successfully!")

if __name__ == "__main__":
    build()
