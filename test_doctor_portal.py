#!/usr/bin/env python3
"""Quick test of doctor portal"""

import subprocess
import sys

# Test the doctor portal with automated inputs
proc = subprocess.Popen(
    [sys.executable, 'doctor_portal.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

try:
    # Login as doctor 1, view menu option 1 (today's schedule), then logout
    output, _ = proc.communicate(input='1\n1\n8\n', timeout=10)
    print(output)
except subprocess.TimeoutExpired:
    proc.kill()
    print('\n[Test timed out - portal may be waiting for more input]')
except Exception as e:
    print(f'\nError: {e}')
