# Define Python environment
PYTHON = venv/bin/python
PIP = venv/bin/pip

# Define app entry point
APP = app.py

# System dependencies for OpenCV (libGL) and general utilities
SYSTEM_DEPENDENCIES = libgl1-mesa-glx libglib2.0-0

all: system-deps venv install-db run

# 1️⃣ Install system dependencies (for OpenCV and GUI support)
system-deps:
	sudo apt-get update && sudo apt-get install -y $(SYSTEM_DEPENDENCIES)

# 2️⃣ Set up virtual environment
venv:
	python3 -m venv venv
	[ -f venv/bin/pip ] || python3 -m ensurepip --default-pip
	$(PIP) install --upgrade pip

# 3️⃣ Install Python dependencies
install:
	$(PIP) install -r requirements.txt
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
