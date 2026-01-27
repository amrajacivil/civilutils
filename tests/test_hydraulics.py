import os
import sys
import unittest
import io
import contextlib

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from civilutils.generic.hydraulics import mannings_discharge



class TestManningsDischarge(unittest.TestCase):
    def test_known_values(self):
        # Known inputs
        n = 0.013
        area = 1.0
        hydraulic_radius = 0.5
        slope = 0.001
        # expected using Manning's formula
        expected = (1.0 / n) * area * (hydraulic_radius ** (2.0 / 3.0)) * (slope ** 0.5)
        result = mannings_discharge(n, area, hydraulic_radius, slope)
        self.assertAlmostEqual(result, expected, places=6)

    def test_zero_area_returns_zero(self):
        n = 0.015
        area = 0.0
        hydraulic_radius = 0.3
        slope = 0.01
        result = mannings_discharge(n, area, hydraulic_radius, slope)
        self.assertEqual(result, 0.0)

    def test_higher_roughness_reduces_discharge(self):
        # same geometry and slope, different Manning's n
        area = 0.8
        R = 0.4
        S = 0.002
        q_low_n = mannings_discharge(0.010, area, R, S)   # smoother
        q_high_n = mannings_discharge(0.020, area, R, S)  # rougher
        self.assertGreater(q_low_n, q_high_n)

    def test_zero_n_raises(self):
        # n = 0 should raise a ZeroDivisionError
        with self.assertRaises(ZeroDivisionError):
            mannings_discharge(0.0, 1.0, 0.5, 0.001)


if __name__ == "__main__":
    unittest.main()