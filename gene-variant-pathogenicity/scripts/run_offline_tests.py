#!/usr/bin/env python3
"""Run regression tests with socket connections disabled in the test process."""
import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

root = Path(__file__).resolve().parents[1]
suite = unittest.defaultTestLoader.discover(str(root / 'tests'))
with patch.object(socket.socket, 'connect', side_effect=AssertionError('offline test: network forbidden')):
    result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
