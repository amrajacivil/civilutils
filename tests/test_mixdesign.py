import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from civilutils.concrete.mixdesign import (
    ISMIXDesign,
    ConcreteGrade,
    MaximumNominalSize,
    MineralAdmixture,
    ExposureCondition,
    SpecificGravity,
    Materials,
)
    


def _make_basic_specific_gravities():
    return [
        SpecificGravity(Materials.CEMENT, 3.15),
        SpecificGravity(Materials.FINE_AGGREGATE, 2.65),
        SpecificGravity(Materials.COARSE_AGGREGATE, 2.70),
        SpecificGravity(Materials.WATER, 1.00),
    ]


class TestCalculateTargetMeanCompressiveStrength(unittest.TestCase):
    def test_target_mean_for_m20(self):
        specific_gravities = _make_basic_specific_gravities()
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M20,
            maximum_nominal_size=MaximumNominalSize.SIZE_20,
            mineral_admixture=MineralAdmixture.FLY_ASH,
            exposure_condition=ExposureCondition.MILD,
            specific_gravities=specific_gravities,
        )

        result = design._calculate_target_mean_compressive_strength()
        # expected = 20 + 1.65 * 4.0 = 26.6
        self.assertAlmostEqual(result, 26.6, places=6)
        self.assertEqual(design.characteristic_strength, 20)
        self.assertAlmostEqual(design.standard_deviation, 4.0)
        self.assertAlmostEqual(design.target_mean_compressive_strength, 26.6, places=6)

    def test_target_mean_for_m10(self):
        specific_gravities = _make_basic_specific_gravities()
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M10,
            maximum_nominal_size=MaximumNominalSize.SIZE_10,
            mineral_admixture=MineralAdmixture.FLY_ASH,
            exposure_condition=ExposureCondition.MODERATE,
            specific_gravities=specific_gravities,
        )

        result = design._calculate_target_mean_compressive_strength()
        # expected = 10 + 1.65 * 3.5 = 15.775
        self.assertAlmostEqual(result, 15.775, places=6)
        self.assertEqual(design.characteristic_strength, 10)
        self.assertAlmostEqual(design.standard_deviation, 3.5)
        self.assertAlmostEqual(design.target_mean_compressive_strength, 15.775, places=6)

    def test_invalid_grade_raises_value_error(self):
        specific_gravities = _make_basic_specific_gravities()
        design = ISMIXDesign(
            concrete_grade="INVALID_GRADE",
            maximum_nominal_size=MaximumNominalSize.SIZE_20,
            mineral_admixture=MineralAdmixture.FLY_ASH,
            exposure_condition=ExposureCondition.SEVERE,
            specific_gravities=specific_gravities,
        )

        with self.assertRaises(ValueError):
            design._calculate_target_mean_compressive_strength()


if __name__ == "__main__":
    unittest.main()
