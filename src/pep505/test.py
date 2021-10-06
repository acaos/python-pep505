#!/usr/bin/env python3

import unittest

from .hook import activate
activate()

from ._test import TestPep505


if __name__ == '__main__':
    unittest.main()
