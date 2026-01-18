"""Concrete Mix Design Package"""
from enum import Enum

class ConcreteGrade(Enum):
    M10 = "M10"
    M15 = "M15"
    M20 = "M20"
    M25 = "M25"
    M30 = "M30"
    M35 = "M35"
    M40 = "M40"
    M45 = "M45"
    M50 = "M50"
    M55 = "M55"

class MaximumNominalSize(Enum):
    SIZE_10 = 10
    SIZE_20 = 20
    SIZE_40 = 40

class CoarseAggregateType(Enum):
    CRUSHED_STONE = "Crushed Stone"
    GRAVEL = "Gravel"
    ROUNDED_GRAVEL = "Rounded Gravel"
    CRUSHED_ANGULAR = "Crushed Angular"

class FineAggregateZone(Enum):
    ZONE_I = "Zone I"
    ZONE_II = "Zone II"
    ZONE_III = "Zone III"
    ZONE_IV = "Zone IV"

class ExposureCondition(Enum):
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    VERY_SEVERE = "Very Severe"
    EXTREME = "Extreme"

class Materials(Enum):
    CEMENT = "Cement"
    FINE_AGGREGATE = "Fine Aggregate"
    COARSE_AGGREGATE = "Coarse Aggregate"
    WATER = "Water"
    ADMIXTURE = "Admixture"

class ChemicalAdmixture(Enum):
    SUPERPLASTICIZER = "Superplasticizer"
    PLASTICIZER = "Plasticizer"

class MineralAdmixture(Enum):
    FLY_ASH = "Fly Ash"
    NO_ADMIXTURE = "No Admixture"

class SpecificGravity:
    def __init__(self, material: Materials, value: float):
        self.material = material
        self.value = value

class ISMIXDesign:
    def __init__(self, concrete_grade: ConcreteGrade, 
                 maximum_nominal_size: MaximumNominalSize,
                 mineral_admixture: MineralAdmixture,
                 exposure_condition: ExposureCondition,
                 specific_gravities: list[SpecificGravity],
                 minimum_cement_content: float | None = None,
                 maximum_cement_content: float | None = None,
                 method_of_placing: str | bool | None = None,
                 coarse_aggregate_type: CoarseAggregateType | None = None,
                 coarse_aggregate_surface_moisture: str | bool | None = None,
                 coarse_aggregate_surface_moisture_value: float | None = None,
                 fine_aggregate_zone: FineAggregateZone | None = None,
                 fine_aggregate_surface_moisture: str | bool | None = None,
                 fine_aggregate_surface_moisture_value: float | None = None,
                 transportation_time: float | None = None):
        self.name = "ISMIX Design"
        self.version = "1.0"
        self.description = "A design methodology for integrated structural and architectural design."
        self.concrete_grade = concrete_grade
        self.maximum_nominal_size = maximum_nominal_size
        self.mineral_admixture = mineral_admixture
        self.exposure_condition = exposure_condition
        self.minimum_cement_content = minimum_cement_content
        self.maximum_cement_content = maximum_cement_content
        

        mandatory_items = {Materials.CEMENT, Materials.COARSE_AGGREGATE, Materials.WATER, Materials.FINE_AGGREGATE}
        if not mandatory_items.issubset({sg.material for sg in specific_gravities}):
            raise ValueError("Missing mandatory specific gravities.")
        self.specific_gravities = specific_gravities

        # pumping / method of placing
        self.pumping = self._parse_yes_no(method_of_placing)

        # coarse aggregate surface moisture
        self.coarse_aggregate_type = coarse_aggregate_type
        self.coarse_aggregate_surface_moisture_present = self._parse_yes_no(coarse_aggregate_surface_moisture)
        if self.coarse_aggregate_surface_moisture_present is True:
            if coarse_aggregate_surface_moisture_value is None:
                raise ValueError("coarse_aggregate_surface_moisture_value required when coarse_aggregate_surface_moisture is 'yes'")
            self.coarse_aggregate_surface_moisture = float(coarse_aggregate_surface_moisture_value)
        elif self.coarse_aggregate_surface_moisture_present is False:
            self.coarse_aggregate_surface_moisture = 0.0
        else:
            self.coarse_aggregate_surface_moisture = None

        # fine aggregate surface moisture
        self.fine_aggregate_zone = fine_aggregate_zone
        self.fine_aggregate_surface_moisture_present = self._parse_yes_no(fine_aggregate_surface_moisture)
        if self.fine_aggregate_surface_moisture_present is True:
            if fine_aggregate_surface_moisture_value is None:
                raise ValueError("fine_aggregate_surface_moisture_value required when fine_aggregate_surface_moisture is 'yes'")
            self.fine_aggregate_surface_moisture = float(fine_aggregate_surface_moisture_value)
        elif self.fine_aggregate_surface_moisture_present is False:
            self.fine_aggregate_surface_moisture = 0.0
        else:
            self.fine_aggregate_surface_moisture = None

        self.transportation_time = transportation_time

    @staticmethod
    def _parse_yes_no(value: str | bool | None) -> bool | None:
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        v = str(value).strip().lower()
        if v in ("yes", "y", "true", "1"):
            return True
        if v in ("no", "n", "false", "0"):
            return False
        raise ValueError("expecting boolean or one of: 'yes','no','y','n'")
    
    def _calculate_target_mean_compressive_strength(self) -> float:
        """
        Compute target mean compressive strength for the selected concrete grade.

        Uses the standard deviations from the provided table:
        - M10, M15 : 3.5 N/mm^2
        - M20, M25 : 4.0 N/mm^2
        - M30, M35, M40, M45, M50, M55 : 5.0 N/mm^2

        Formula used: target_mean = f_ck + 1.65 * standard_deviation
        (1.65 corresponds to approximately 95% probability / 5% risk)
        """
        std_dev_map = {
            ConcreteGrade.M10: 3.5,
            ConcreteGrade.M15: 3.5,
            ConcreteGrade.M20: 4.0,
            ConcreteGrade.M25: 4.0,
            ConcreteGrade.M30: 5.0,
            ConcreteGrade.M35: 5.0,
            ConcreteGrade.M40: 5.0,
            ConcreteGrade.M45: 5.0,
            ConcreteGrade.M50: 5.0,
            ConcreteGrade.M55: 5.0,
        }

        if self.concrete_grade not in std_dev_map:
            raise ValueError(f"Standard deviation not defined for grade {self.concrete_grade}")

        s = std_dev_map[self.concrete_grade]
        try:
            fck = int(str(self.concrete_grade.value).lstrip("M").strip())
        except Exception:
            # fallback to enum name
            fck = int(self.concrete_grade.name.lstrip("M"))

        target_mean = fck + 1.65 * s
        self.characteristic_strength = fck
        self.standard_deviation = s
        self.target_mean_compressive_strength = target_mean

        return target_mean

    def calculate(self):
        target_mean_strength = self._calculate_target_mean_compressive_strength()


