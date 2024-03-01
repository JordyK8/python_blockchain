import os
from pathlib import Path 

PROJECT_NAME = "python_blockchain_ENX" #add your project name here

LIST_FILES = [
    "Dockerfile",
    ".env",
    ".gitignore",
    "app.py",
    "README.md",
    "requirements.txt",
    "src/__init__.py",
    # config folder
    "src/config/__init__.py",
    "src/config/config.py",
    "src/config/dev_config.py",
    "src/config/production_config.py",
    # controllers
    "src/controllers/__init__.py",
    # middlewares
    "src/middlewares/__init__.py",
    # models
    "src/models/__init__.py",
    # services
    "src/services/__init__.py",
    # routes
     "src/routes.py",
    # utils
     "src/utils/__init__.py",
   ]

for file_path in LIST_FILES:
    file_path = Path(file_path)
    file_dir, file_name = os.path.split(file_path)

    # first make dir
    if file_dir!="":
        os.makedirs(file_dir, exist_ok= True)
        print(f"Creating Directory: {file_dir} for file: {file_name}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path)==0):
        with open(file_path, "w") as f:
            pass
            print(f"Creating an empty file: {file_path}")
    else:
        print(f"File already exists {file_path}")