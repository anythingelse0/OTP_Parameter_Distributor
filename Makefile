# OTP Distributor Generator Makefile
# Works with Git Bash, MinGW, or Cygwin on Windows

PYTHON := python
SCRIPT := src/dynamic_signal_parser.py
INPUT_DIR := input
OUTPUT_DIR := generated

# Default target
.PHONY: help
help:
	@echo "OTP Distributor Generator"
	@echo ""
	@echo "Usage:"
	@echo "  make cygnet         - Generate from cygnetpluse_otp_map.txt"
	@echo "  make csv            - Generate from my_signal.csv"
	@echo "  make all            - Generate all input files"
	@echo "  make clean          - Clean generated files"
	@echo "  make list           - List available input files"
	@echo "  make test           - Run all tests with coverage"
	@echo "  make test-verbose   - Run tests with verbose output"
	@echo "  make test-html      - Generate HTML coverage report"

# Generate from cygnetpluse_otp_map.txt
.PHONY: cygnet
cygnet:
	$(PYTHON) $(SCRIPT) -i $(INPUT_DIR)/cygnetpluse_otp_map.txt -o cygnetpluse_otp_distributor.sv

# Generate from my_signal.csv
.PHONY: csv
csv:
	$(PYTHON) $(SCRIPT) -i $(INPUT_DIR)/my_signal.csv -o my_distributor.sv

# Generate from my_signal2.txt
.PHONY: input2
input2:
	$(PYTHON) $(SCRIPT) -i $(INPUT_DIR)/my_signal2.txt -o my_distributor2.sv

# Generate all
.PHONY: all
all: cygnet csv input2
	@echo "All files generated!"

# Clean generated files (keep .gitignore)
.PHONY: clean
clean:
	rm -f $(OUTPUT_DIR)/*.sv
	rm -f $(OUTPUT_DIR)/*.xlsx
	@echo "Cleaned generated files!"

# Run all tests with coverage (一键回归)
.PHONY: test
test:
	@echo "Running regression tests..."
	$(PYTHON) -m coverage run -m unittest discover tests
	$(PYTHON) -m coverage report --include=src/dynamic_signal_parser.py

# Run tests with verbose output
.PHONY: test-verbose
test-verbose:
	@echo "Running regression tests (verbose)..."
	$(PYTHON) -m coverage run -m unittest discover tests -v
	$(PYTHON) -m coverage report --include=src/dynamic_signal_parser.py

# Generate HTML coverage report
.PHONY: test-html
test-html:
	@echo "Running regression tests and generating HTML report..."
	$(PYTHON) -m coverage run -m unittest discover tests
	$(PYTHON) -m coverage html --include=src/dynamic_signal_parser.py -d coverage_html
	@echo "HTML coverage report generated in coverage_html/"

# List available input files
.PHONY: list
list:
	@echo "Available input files:"
	@ls -1 $(INPUT_DIR)/*.* 2>/dev/null || dir /b $(INPUT_DIR)

# Custom generation - usage: make gen INPUT=input/myfile.txt OUTPUT=myout.sv
.PHONY: gen
gen:
	@if [ -z "$(INPUT)" ]; then \
		echo "Error: INPUT not specified"; \
		echo "Usage: make gen INPUT=input/myfile.txt OUTPUT=myout.sv"; \
		exit 1; \
	fi
	$(PYTHON) $(SCRIPT) -i $(INPUT) -o $(OUTPUT)
