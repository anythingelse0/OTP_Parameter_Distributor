#!/usr/bin/env python3
"""
OTP Distributor Generator - Quick wrapper script
Usage: python generate.py [input_file] [output_name]

Examples:
    python generate.py input/cygnetpluse_otp_map.txt cygnetpluse_otp_distributor.sv
    python generate.py input/my_signal.csv my_distributor.sv
"""

import sys
import os

# Default input/output
DEFAULT_INPUT = "input/cygnetpluse_otp_map.txt"
DEFAULT_OUTPUT = "cygnetpluse_otp_distributor.sv"

def main():
    # Parse arguments
    input_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    output_name = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT

    # Fix path separator for Windows
    input_file = input_file.replace('/', os.sep)

    # Build command
    script_path = os.path.join("src", "dynamic_signal_parser.py")
    cmd = f'python "{script_path}" -i "{input_file}" -o "{output_name}"'

    print(f"=" * 50)
    print(f"  OTP Distributor Generator")
    print(f"=" * 50)
    print(f"  Input:  {input_file}")
    print(f"  Output: generated/{output_name}")
    print(f"=" * 50)
    print()

    # Execute
    os.system(cmd)

if __name__ == "__main__":
    main()
