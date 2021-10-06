#!/usr/bin/env python3

import unittest

class TestPep505(unittest.TestCase):
    def test_coalesce_simple(self):
        self.assertTrue(None ?? True)

    def test_coalesce_chain(self):
        self.assertTrue(None ?? None ?? True ?? False)

    def test_coalesce_in_subscript(self):
        l = [1, 2]
        self.assertEqual(l[None ?? 0], 1)

    def test_maybe_assign_simple(self):
        x = None
        x ??= True
        self.assertTrue(x)

    def test_maybe_dot_simple(self):
        self.assertIsNone(None?.foo)

    def test_maybe_subscript_simple(self):
        self.assertIsNone(None?[0])

    def test_complex(self):
        self.assertTrue(None?.foo?[0]?.foo ?? None ?? True ?? False)

