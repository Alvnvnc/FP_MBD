	# Makefile for Python-Streamlit app

# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
STREAMLIT = $(VENV_DIR)/bin/streamlit

# Default target
all: setup run

# Create virtual environment
$(VENV_DIR):
	python3 -m venv $(VENV_DIR)

# Install dependencies
install: $(VENV_DIR)
	$(PIP) install -r requirements.txt

# Setup database (if required)
setup-db: install
	$(PYTHON) setup_database.py

# Run the application
run: install
	$(STREAMLIT) run app.py

# Delete tables
# delete-tables: install
# 	$(PYTHON) delete_tables.py

# Custom functions (if any)
functions: install
	$(PYTHON) function.py

# Custom procedures (if any)
procedures: install
	$(PYTHON) procedures.py

# Custom triggers (if any)
triggers: install
	$(PYTHON) trigger.py

# Custom input (if any)
input: install
	$(PYTHON) input.py

# Terminal commands (if any)
terminal: install
	$(PYTHON) terminal.py

# Clean up virtual environment
clean:
	rm -rf $(VENV_DIR)

# Help message
help:
	@echo "Makefile for Python-Streamlit app"
	@echo ""
	@echo "Usage:"
	@echo "  make            Create virtual environment, install dependencies, and run the app"
	@echo "  make install    Install dependencies"
	@echo "  make setup-db   Set up the database"
	@echo "  make run        Run the application"
	@echo "  make clean      Clean up virtual environment"
	@echo "  make help       Show this help message"
	@echo "  make delete-tables  Delete tables"
	@echo "  make truncate-tables  Truncate tables"
	@echo "  make functions  Run custom functions"
	@echo "  make procedures Run custom procedures"
	@echo "  make triggers   Run custom triggers"
	@echo "  make input      Run custom input script"
	@echo "  make terminal   Run terminal commands"
