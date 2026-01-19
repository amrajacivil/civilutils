"""Concrete Mix Design Package"""
from enum import Enum

class ConcreteGrade(Enum):
    """Concrete grades as per IS 456.

    Args:
        Enum (str): The concrete grade designation.
    """    
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

class CementGrade(Enum):
    """Cement grades as per IS 456.

    Args:
        Enum (str): The cement grade designation.
    """
    OPC_33 = "OPC 33"
    OPC_43 = "OPC 43"
    OPC_53 = "OPC 53"
    PPC = "PPC"
    PSC = "PSC"

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
    """Fine aggregate zones as per IS 456.

    Args:
        Enum (str): The fine aggregate zone designation.
    """
    ZONE_I = "Zone I"
    ZONE_II = "Zone II"
    ZONE_III = "Zone III"
    ZONE_IV = "Zone IV"

class ExposureCondition(Enum):
    """
    Environmental exposure categories based on IS456 (Table 3).

    These categories are used to select design limits (for example maximum
    water/cement ratio, minimum cement content and cover) according to the
    service environment the concrete will face.

    Members:
    - MILD: Concrete surfaces protected against weather or aggressive
      conditions (e.g., sheltered or protected locations).
    - MODERATE: Exposed to condensation, rain or continuous wetting (including
      contact with non-aggressive soil/ground water); sheltered from severe
      weather.
    - SEVERE: Exposed to severe rain, alternate wetting and drying, occasional
      freezing when wet, immersion in seawater or coastal environment, or
      saturated salt air.
    - VERY_SEVERE: Exposed to sea water spray, corrosive fumes, severe freezing,
      or concrete in contact with or buried under aggressive subsoil/ground
      water.
    - EXTREME: Members in tidal zones or in direct contact with liquid or solid
      aggressive chemicals.
    """
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
    """Chemical admixtures as per IS 456.

    Args:
        Enum (str): The chemical admixture designation.
    """ 
    SUPERPLASTICIZER = "Superplasticizer"
    PLASTICIZER = "Plasticizer"

class MineralAdmixture(Enum):
    """Mineral admixtures as per IS 456.

    Args:
        Enum (str): The mineral admixture designation.
    """
    FLY_ASH = "Fly Ash"
    NO_ADMIXTURE = "No Admixture"

class SpecificGravity:
    """Specific gravity of materials as per IS 456.
    """
    def __init__(self, material: Materials, value: float):
        self.material = material
        self.value = value

class ISMIXDesign:
    def __init__(self, concrete_grade: ConcreteGrade,
                 maximum_nominal_size: MaximumNominalSize,
                 mineral_admixture: MineralAdmixture,
                 exposure_condition: ExposureCondition,
                 specific_gravities: list[SpecificGravity],
                 cement_grade: CementGrade | None = None,
                 minimum_cement_content: float | None = None,
                 maximum_cement_content: float | None = None,
                 method_of_placing: str | bool | None = None,
                 chemical_admixture: ChemicalAdmixture | None = None,
                 coarse_aggregate_type: CoarseAggregateType | None = None,
                 coarse_aggregate_surface_moisture: str | bool | None = None,
                 coarse_aggregate_surface_moisture_value: float | None = None,
                 fine_aggregate_zone: FineAggregateZone | None = None,
                 fine_aggregate_surface_moisture: str | bool | None = None,
                 fine_aggregate_surface_moisture_value: float | None = None,
                 transportation_time: float | None = None,
                 slump_mm: float | None = 50.0):
        self.description = "A design methodology for integrated structural and architectural design."
        self.concrete_grade = concrete_grade
        self.maximum_nominal_size = maximum_nominal_size
        self.mineral_admixture = mineral_admixture
        self.exposure_condition = exposure_condition
        # slump (mm) used to adjust water content; reference table is for 50 mm
        self.slump_mm = float(slump_mm) if slump_mm is not None else None
        # fraction change per 25 mm (e.g. 0.03 == 3% change per 25 mm)
        self.slump_adjustment_pct_per_25mm = 0.03
        self.minimum_cement_content = minimum_cement_content
        self.maximum_cement_content = maximum_cement_content
        self.cement_grade = cement_grade
        self.chemical_admixture = chemical_admixture

        mandatory_items = {Materials.CEMENT, Materials.COARSE_AGGREGATE, Materials.WATER, Materials.FINE_AGGREGATE}
        # Accept either a list[SpecificGravity] or a dict[Materials, SpecificGravity]
        if isinstance(specific_gravities, dict):
            sg_map = specific_gravities
        else:
            sg_map = {sg.material: sg for sg in specific_gravities}
        if not mandatory_items.issubset(set(sg_map.keys())):
            raise ValueError("Missing mandatory specific gravities.")
        self.specific_gravities = sg_map

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

    def _calculate_water_cement_ratio_by_is456(self, reinforced: bool = True) -> float:
        """
        Determine maximum water/cement ratio from IS456 Table 5 for
        normal-weight aggregates of 20 mm nominal maximum size.

        Returns and sets self.maximum_water_cement_ratio.

        Table values (maximum free water-cement ratio):
        - Plain concrete:    Mild 0.60, Moderate 0.60, Severe 0.50, Very severe 0.45, Extreme 0.40
        - Reinforced concrete:Mild 0.55, Moderate 0.50, Severe 0.45, Very severe 0.45, Extreme 0.40
        """
        if self.exposure_condition is None:
            raise ValueError("exposure_condition must be set to determine water/cement ratio")

        plain_map = {
            ExposureCondition.MILD: 0.60,
            ExposureCondition.MODERATE: 0.60,
            ExposureCondition.SEVERE: 0.50,
            ExposureCondition.VERY_SEVERE: 0.45,
            ExposureCondition.EXTREME: 0.40,
        }
        reinforced_map = {
            ExposureCondition.MILD: 0.55,
            ExposureCondition.MODERATE: 0.50,
            ExposureCondition.SEVERE: 0.45,
            ExposureCondition.VERY_SEVERE: 0.45,
            ExposureCondition.EXTREME: 0.40,
        }
        mapping = reinforced_map if reinforced else plain_map
        wcr = mapping[self.exposure_condition]
        if self.mineral_admixture != MineralAdmixture.NO_ADMIXTURE:
            wcr -= 0.05
        self.maximum_water_cement_ratio = float(wcr)
        return self.maximum_water_cement_ratio

    def _calculate_water_content(self):
        """
        Determine reference water content (kg/m^3) based on nominal maximum
        aggregate size (IS table).
        10 mm -> 208, 20 mm -> 186, 40 mm -> 165
        Stores and returns self.maximum_water_content.

        Reference table values correspond to 50 mm slump. If self.slump_mm is
        provided the water content is adjusted by slump_adjustment_pct_per_25mm
        for every 25 mm difference from 50 mm.

        If superplasticizer is used, the water content is reduced by 20%.
        """
        if self.maximum_nominal_size is None:
            raise ValueError("maximum_nominal_size must be set to determine water content")

        mapping = {
            MaximumNominalSize.SIZE_10: 208.0,
            MaximumNominalSize.SIZE_20: 186.0,
            MaximumNominalSize.SIZE_40: 165.0,
        }

        base_water = float(mapping[self.maximum_nominal_size])
        if self.slump_mm is not None:
            steps = (self.slump_mm - 50.0) / 25.0  # positive if slump > 50, negative if < 50
            adjusted_water = base_water * (1.0 + steps * self.slump_adjustment_pct_per_25mm)
        else:
            adjusted_water = base_water

        if self.chemical_admixture == ChemicalAdmixture.SUPERPLASTICIZER:
            adjusted_water *= 0.8

        self.maximum_water_content = adjusted_water
        return adjusted_water

    
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

        s = std_dev_map[self.concrete_grade]
        try:
            fck = int(str(self.concrete_grade.value).lstrip("M").strip())
        except Exception:
            fck = int(self.concrete_grade.name.lstrip("M"))

        target_mean = fck + 1.65 * s
        self.characteristic_strength = fck
        self.standard_deviation = s
        self.target_mean_compressive_strength = target_mean
        return target_mean

    def __calculate_cement_content(self, water_cement_ratio, water_content):
        MINIMUM_CEMENT_CONTENT_BY_EXPOSURE = {
            ExposureCondition.MILD: 300.0,
            ExposureCondition.MODERATE: 300.0,
            ExposureCondition.SEVERE: 320.0,
            ExposureCondition.VERY_SEVERE: 340.0,
            ExposureCondition.EXTREME: 360.0,
        }
        minimum_cement_content = MINIMUM_CEMENT_CONTENT_BY_EXPOSURE[self.exposure_condition]
        cement_content= water_content / water_cement_ratio
        self.minimum_cement_content = max(cement_content, minimum_cement_content)   
        return self.minimum_cement_content
    
    def __calculate_aggregate_content(self):
        """Determine volume fraction of coarse aggregate per unit volume of
        total aggregate from IS table (Table 3) depending on fine aggregate
        zone and nominal maximum size.

        Raises:
            ValueError: If fine_aggregate_zone or maximum_nominal_size is not set.
            ValueError: If unsupported combination of maximum_nominal_size and fine_aggregate_zone is used.

        Returns:
            float: Proportion of coarse aggregate.
        """
        if self.fine_aggregate_zone is None or self.maximum_nominal_size is None:
            raise ValueError("fine_aggregate_zone and maximum_nominal_size must be set to determine coarse aggregate proportion")

        table = {
            MaximumNominalSize.SIZE_10: {
                FineAggregateZone.ZONE_IV: 0.50,
                FineAggregateZone.ZONE_III: 0.48,
                FineAggregateZone.ZONE_II: 0.46,
                FineAggregateZone.ZONE_I: 0.44,
            },
            MaximumNominalSize.SIZE_20: {
                FineAggregateZone.ZONE_IV: 0.66,
                FineAggregateZone.ZONE_III: 0.64,
                FineAggregateZone.ZONE_II: 0.62,
                FineAggregateZone.ZONE_I: 0.60,
            },
            MaximumNominalSize.SIZE_40: {
                FineAggregateZone.ZONE_IV: 0.75,
                FineAggregateZone.ZONE_III: 0.73,
                FineAggregateZone.ZONE_II: 0.71,
                FineAggregateZone.ZONE_I: 0.69,
            },
        }

        try:
            prop = table[self.maximum_nominal_size][self.fine_aggregate_zone]
        except KeyError:
            raise ValueError("unsupported combination of maximum_nominal_size and fine_aggregate_zone")

        self.coarse_aggregate_proportion = float(prop)
        if self.water_cement_ratio == 0.5:
            self.coarse_aggregate_proportion = float(prop)
        elif self.water_cement_ratio < 0.5:
            decrease = (0.5 - self.water_cement_ratio) / 0.05
            self.coarse_aggregate_proportion = float(prop) + decrease * 0.01
        else:
            increase = (self.water_cement_ratio - 0.5) / 0.05
            self.coarse_aggregate_proportion = float(prop) - increase * 0.01

        if self.is_pumpable:
            self.coarse_aggregate_proportion *= 0.9

        fine_aggregate_proportion = 1 - self.coarse_aggregate_proportion
        self.fine_aggregate_proportion = float(fine_aggregate_proportion)

        return self.coarse_aggregate_proportion, self.fine_aggregate_proportion

    def calculate_volume_based_on_mass_and_specific_gravity(self,mass,specific_gravity):
        """Calculate the volume based on mass and specific gravity.

        Args:
            mass (float): The mass of the material.
            specific_gravity (float): The specific gravity of the material.

        Returns:
            float: The volume of the material.
        """        
        volume = (mass / specific_gravity) * (1/1000)
        return volume

    def get_specific_gravity(self, material: Materials) -> float:
        """Return the numeric specific gravity for a given material (raises if missing)."""
        sg = self.specific_gravities.get(material)
        if sg is None:
            raise ValueError(f"specific gravity for {material} not provided")
        return float(sg.value)

    def calculate(self):
        target_mean_strength = self._calculate_target_mean_compressive_strength()
        water_cement_ratio = self._calculate_water_cement_ratio_by_is456()
        water_content = self._calculate_water_content()
        cement_content = self.__calculate_cement_content(water_cement_ratio, water_content)
        coarse_aggregate_proportion, fine_aggregate_proportion = self.__calculate_aggregate_content()

        volume_of_concrete=1
        volume_of_cement = self.calculate_volume_based_on_mass_and_specific_gravity(
            cement_content, self.get_specific_gravity(Materials.CEMENT)
        )
        volume_of_water = self.calculate_volume_based_on_mass_and_specific_gravity(
            water_content, self.get_specific_gravity(Materials.WATER)
        )
        # admixture content is 1.1% of cement content
        self.admixture_content = 0.011 * cement_content
        volume_of_admixture = self.calculate_volume_based_on_mass_and_specific_gravity(
            self.admixture_content, self.get_specific_gravity(Materials.ADMIXTURE)
        )
        volume_of_all_in_aggregate=1-volume_of_cement - volume_of_water - volume_of_admixture

        self.coarse_aggregate_content = volume_of_all_in_aggregate * coarse_aggregate_proportion \
                                    * self.get_specific_gravity(Materials.COARSE_AGGREGATE) * 1000
        self.fine_aggregate_content = volume_of_all_in_aggregate * fine_aggregate_proportion \
                                    * self.get_specific_gravity(Materials.FINE_AGGREGATE) * 1000

        return {
            "target_mean_strength": target_mean_strength,
            "water_cement_ratio": water_cement_ratio,
            "water_content": water_content,
            "cement_content": cement_content,
            "coarse_aggregate_content": coarse_aggregate_proportion,
            "fine_aggregate_content": fine_aggregate_proportion,
        }

