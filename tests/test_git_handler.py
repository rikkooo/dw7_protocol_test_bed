import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add src to path to allow importing git_handler
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dw6 import git_handler



if __name__ == '__main__':
    unittest.main()
