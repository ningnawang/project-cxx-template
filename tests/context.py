import numpy as np
import gpytoolbox as gpy
import os, sys

# Make the repo root and utility/ importable.
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(_REPO_ROOT)
sys.path.append(os.path.join(_REPO_ROOT, 'utility'))

# The Python utilities live in utility/python_utils; expose them as `utility`.
import python_utils as utility
import unittest