#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- parsing: pep505 -*-

import unittest

class TestPep505(unittest.TestCase):
    def notcalled(self):
        self._notcalled = False

    def test_coalesce_simple(self):
        self.assertTrue(None ?? True)

    def test_coalesce_chain(self):
        self.assertTrue(None ?? None ?? True ?? False)

    def test_coalesce_in_subscript(self):
        l = [1, 2]
        self.assertEqual(l[None ?? 0], 1)

    def test_coalesce_not_evaluated(self):
        self._notcalled = True
        x = True ?? self.notcalled()
        self.assertTrue(self._notcalled)

    def test_maybe_assign_simple(self):
        x = None
        x ??= True
        self.assertTrue(x)

    def test_maybe_assign_not_evaluated(self):
        self._notcalled = True
        x = True
        x ??= self.notcalled()
        self.assertTrue(self._notcalled)

    def test_maybe_dot_simple(self):
        self.assertIsNone(None?.foo)

    def test_maybe_subscript_simple(self):
        self.assertIsNone(None?[0])

    def test_maybe_subscript_not_evaluated(self):
        self._notcalled = True
        x = None?[self.notcalled()]
        self.assertTrue(self._notcalled)

    def test_complex(self):
        self.assertTrue(None?.foo?[0]?.foo ?? None ?? True ?? False)

    def test_precedence_add(self):
        x = 2 + None ?? 2
        self.assertEqual(x, 4)

    def test_precedence_negative(self):
        x = 2 + None ?? -2
        self.assertEqual(x, 0)

    def test_precedence_multiply(self):
        x = 2 * None ?? 4
        self.assertEqual(x, 8)

    def test_precedence_power(self):
        x = 2 ** None ?? 4
        self.assertEqual(x, 16)

    def test_precedence_chained(self):
        x = 2 ** None ?? 4 + 16
        self.assertEqual(x, 32)

    def test_precedence_chained_powers(self):
        x = 2 ** None ?? 3 ** 4
        self.assertEqual(x, 2417851639229258349412352)

