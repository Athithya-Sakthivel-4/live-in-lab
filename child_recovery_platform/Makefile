# Define Python environment paths
PYTHON = .venv/bin/python
PIP = .venv/bin/pip
UVICORN = .venv/bin/uvicorn

# Define app entry point
APP = app.py

# System dependencies (Linux & macOS)
SYSTEM_DEPENDENCIES = libgl1 libglib2.0-0 mesa-utils
MAC_DEPENDENCIES = opencv

# 1️⃣ Run everything in one step
all: system-deps venv install-db run

# 2️⃣ Install system dependencies automatically
system-deps:
	@echo "🔍 Detecting OS..."
	@if [ -f "/etc/debian_version" ]; then \
		echo "📦 Installing system dependencies for Debian-based OS"; \
		sudo apt-get update && sudo apt-get install -y $(SYSTEM_DEPENDENCIES); \
	elif [ "$$(uname)" = "Darwin" ]; then \
		echo "🍏 Installing dependencies for macOS"; \
		brew install $(MAC_DEPENDENCIES); \
	else \
		echo "⚠️ Unsupported OS. Please install dependencies manually."; \
		exit 1; \
	fi

# 3️⃣ Set up virtual environment
venv:
	@echo "🛠️ Setting up virtual environment..."
	rm -rf .venv  # Ensure fresh environment
	python3 -m venv .venv
	. .venv/bin/activate && $(PIP) install --upgrade pip setuptools wheel


# 4️⃣ Install Python dependencies
install:
	@echo "📦 Installing Python dependencies..."
	$(PIP) install --no-cache-dir -r requirements.txt
	$(PIP) cache purge  # Clean cache

# 5️⃣ Initialize database (after installing dependencies)
install-db: install
	@echo "🗂️ Setting up database..."
	$(PYTHON) database.py

# 6️⃣ Run the FastAPI application with Uvicorn
run:
	@echo "🚀 Starting FastAPI server..."
	$(UVICORN) app:app --host 0.0.0.0 --port 8000 --reload

# 7️⃣ Clean up the environment
clean:
	@echo "🧹 Cleaning up environment..."
	rm -rf .venv __pycache__ *.pyc *.pyo children.db
