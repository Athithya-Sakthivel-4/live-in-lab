# Define Python environment
PYTHON = venv/bin/python
PIP = venv/bin/pip

# Define app entry point
APP = app.py

# System dependencies for OpenCV and general utilities
SYSTEM_DEPENDENCIES = libgl1 libglib2.0-0 mesa-utils

all: system-deps venv install-db run

# 1️⃣ Install system dependencies (for OpenCV and GUI support)
system-deps:
	sudo apt-get update && sudo apt-get install -y $(SYSTEM_DEPENDENCIES)
	sudo apt-get install -y python3.11 python3.11-venv python3.11-dev
	python3.11 -m pip install --upgrade pip setuptools wheel

# 2️⃣ Set up a fresh virtual environment
venv:
	rm -rf venv  # Ensure a fresh environment
	python3.11 -m venv venv
	$(PIP) install --upgrade pip
	pip3 cache purge

# 3️⃣ Install Python dependencies
install:
	$(PIP) install --no-cache-dir -r requirements.txt
	$(PIP) install tf-keras  # Fix DeepFace error

# 4️⃣ Initialize database
install-db: install
	$(PYTHON) database.py

# 5️⃣ Run the application
run:
	$(PYTHON) $(APP)

# 6️⃣ Clean up environment
clean:
	rm -rf venv __pycache__ *.pyc *.pyo
	rm -f children.db
