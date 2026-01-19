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


    def test_reinforced_severe_no_admixture(self):
        """Reinforced, SEVERE exposure, no mineral admixture -> 0.45"""
        specific_gravities = _make_basic_specific_gravities()
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M25,
            maximum_nominal_size=MaximumNominalSize.SIZE_20,
            mineral_admixture=MineralAdmixture.NO_ADMIXTURE,
            exposure_condition=ExposureCondition.SEVERE,
            specific_gravities=specific_gravities,
        )

        result = design._calculate_water_cement_ratio_by_is456(reinforced=True)
        self.assertAlmostEqual(result, 0.45, places=6)
        self.assertAlmostEqual(design.maximum_water_cement_ratio, 0.45, places=6)

    def test_plain_moderate_with_admixture(self):
        """Plain concrete, MODERATE exposure, has mineral admixture -> plain 0.60 minus 0.05 = 0.55"""
        specific_gravities = _make_basic_specific_gravities()
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M20,
            maximum_nominal_size=MaximumNominalSize.SIZE_20,
            mineral_admixture=MineralAdmixture.FLY_ASH,
            exposure_condition=ExposureCondition.MODERATE,
            specific_gravities=specific_gravities,
        )

        result = design._calculate_water_cement_ratio_by_is456(reinforced=False)
        self.assertAlmostEqual(result, 0.55, places=6)
        self.assertAlmostEqual(design.maximum_water_cement_ratio, 0.55, places=6)

    def test_calculate_water_content(self):
        specific_gravities = _make_basic_specific_gravities()

        # base values for nominal sizes
        expected_map = {
            MaximumNominalSize.SIZE_10: 208.0,
            MaximumNominalSize.SIZE_20: 186.0,
            MaximumNominalSize.SIZE_40: 165.0,
        }
        for size, expected in expected_map.items():
            with self.subTest(size=size):
                design = ISMIXDesign(
                    concrete_grade=ConcreteGrade.M20,
                    maximum_nominal_size=size,
                    mineral_admixture=MineralAdmixture.NO_ADMIXTURE,
                    exposure_condition=ExposureCondition.MILD,
                    specific_gravities=specific_gravities,
                )
                result = design._calculate_water_content()
                self.assertAlmostEqual(result, expected, places=6)
                self.assertAlmostEqual(design.maximum_water_content, expected, places=6)

        # slump increase (75 mm) with 3% adjustment per 25 mm
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M20,
            maximum_nominal_size=MaximumNominalSize.SIZE_20,
            mineral_admixture=MineralAdmixture.NO_ADMIXTURE,
            exposure_condition=ExposureCondition.MILD,
            specific_gravities=specific_gravities,
            slump_mm=75.0,
            
        )
        # base 186 -> one step up (25 mm) -> 186 * 1.03 = 191.58
        self.assertAlmostEqual(design._calculate_water_content(), 191.58, places=6)

        # slump decrease (25 mm) with 3% adjustment per 25 mm
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M20,
            maximum_nominal_size=MaximumNominalSize.SIZE_20,
            mineral_admixture=MineralAdmixture.NO_ADMIXTURE,
            exposure_condition=ExposureCondition.MILD,
            specific_gravities=specific_gravities,
            slump_mm=25.0,
        )
        # base 186 -> one step down -> 186 * 0.97 = 180.42
        self.assertAlmostEqual(design._calculate_water_content(), 180.42, places=6)

        # superplasticizer reduces water by 20%
        from civilutils.concrete.mixdesign import ChemicalAdmixture
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M20,
            maximum_nominal_size=MaximumNominalSize.SIZE_20,
            mineral_admixture=MineralAdmixture.NO_ADMIXTURE,
            exposure_condition=ExposureCondition.MILD,
            specific_gravities=specific_gravities,
            chemical_admixture=ChemicalAdmixture.SUPERPLASTICIZER,
        )
        # base 186 * 0.8 = 148.8
        self.assertAlmostEqual(design._calculate_water_content(), 148.8, places=6)

        # missing maximum_nominal_size raises
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M20,
            maximum_nominal_size=None,
            mineral_admixture=MineralAdmixture.NO_ADMIXTURE,
            exposure_condition=ExposureCondition.MILD,
            specific_gravities=specific_gravities,
        )
        with self.assertRaises(ValueError):
            design._calculate_water_content()

    def test_get_specific_gravity_missing_raises(self):
        """Requesting SG for a material not provided should raise."""
        specific_gravities = _make_basic_specific_gravities()
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M20,
            maximum_nominal_size=MaximumNominalSize.SIZE_20,
            mineral_admixture=MineralAdmixture.NO_ADMIXTURE,
            exposure_condition=ExposureCondition.MILD,
            specific_gravities=specific_gravities,
        )
        with self.assertRaises(ValueError):
            design.get_specific_gravity(Materials.ADMIXTURE)

    def test_accepts_dict_specific_gravities(self):
        """ISMIXDesign should accept a dict of SpecificGravity keyed by Materials."""
        sg_dict = {
            Materials.CEMENT: SpecificGravity(Materials.CEMENT, 3.15),
            Materials.FINE_AGGREGATE: SpecificGravity(Materials.FINE_AGGREGATE, 2.65),
            Materials.COARSE_AGGREGATE: SpecificGravity(Materials.COARSE_AGGREGATE, 2.70),
            Materials.WATER: SpecificGravity(Materials.WATER, 1.00),
        }
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M20,
            maximum_nominal_size=MaximumNominalSize.SIZE_20,
            mineral_admixture=MineralAdmixture.NO_ADMIXTURE,
            exposure_condition=ExposureCondition.MILD,
            specific_gravities=sg_dict,
        )
        self.assertAlmostEqual(design.get_specific_gravity(Materials.CEMENT), 3.15, places=6)

    def test_volume_calculation(self):
        """Basic sanity for calculate_volume_based_on_mass_and_specific_gravity."""
        specific_gravities = _make_basic_specific_gravities()
        design = ISMIXDesign(
            concrete_grade=ConcreteGrade.M20,
            maximum_nominal_size=MaximumNominalSize.SIZE_20,
            mineral_admixture=MineralAdmixture.NO_ADMIXTURE,
            exposure_condition=ExposureCondition.MILD,
            specific_gravities=specific_gravities,
        )
        # mass 1000, sg 2.0 -> volume = (1000/2.0) * 0.001 = 0.5 m^3
        self.assertAlmostEqual(design.calculate_volume_based_on_mass_and_specific_gravity(1000.0, 2.0), 0.5, places=6)

if __name__ == "__main__":
    unittest.main()
