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

class MaximumNominalSize(Enum):
    """Maximum nominal sizes of aggregates as per IS 456.

    Args:
        Enum (int): The maximum nominal size in mm.
    """    
    SIZE_10 = 10
    SIZE_20 = 20
    SIZE_40 = 40

class CoarseAggregateType(Enum):
    """Coarse aggregate types as per IS 456.

    Args:
        Enum (str): The coarse aggregate type designation.
    """    
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
    """Material types as per IS 456.

    Args:
        Enum (str): The material designation.
    """    
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
    PLASTICIZER = "Plasticizer" #TODO: find and implement logic

    def __init__(self, label: str, default_percentage: float = 20.0):
        self.label = label
        self.default_percentage = float(default_percentage)

class MineralAdmixture(Enum):
    """Mineral admixtures as per IS 456.

    Args:
        Enum (str): The mineral admixture designation.
    """
    FLY_ASH = ("Fly Ash", 10.0)        # default percentage (e.g. % replacement of cement)

    def __init__(self, label: str, default_percentage: float = 0.0):
        self.label = label
        self.default_percentage = float(default_percentage)

class SpecificGravity:
    """Specific gravity of materials as per IS 456.
    """
    def __init__(self, material: Materials, value: float):
        self.material = material
        self.value = value

class ConcreteMixDesign:
    """Concrete mix design parameters as per IS 10262 and IS 456.
    """
    def __init__(self, concrete_grade: ConcreteGrade,
                 exposure_condition: ExposureCondition,
                 specific_gravities: list[SpecificGravity],
                 maximum_nominal_size: MaximumNominalSize = MaximumNominalSize.SIZE_20,
                 maximum_cement_content: float = 450.0,
                 is_pumpable: str | bool = True ,
                 chemical_admixture: ChemicalAdmixture | None = None,
                 chemical_admixture_percentage: float | None = None,
                 coarse_aggregate_type: CoarseAggregateType = CoarseAggregateType.CRUSHED_ANGULAR,
                 coarse_aggregate_water_absorption: float = 0.0,
                 coarse_aggregate_surface_moisture: float = 0.0,
                 fine_aggregate_zone: FineAggregateZone = FineAggregateZone.ZONE_II,
                 fine_aggregate_surface_moisture: float = 0.0,
                 fine_aggregate_water_absorption: float = 0.0,
                 slump_mm: float  = 50.0,
                 mineral_admixture: MineralAdmixture | None = None,
                 mineral_admixture_percentage: float | None = None):
        self.concrete_grade = concrete_grade
        self.maximum_nominal_size = maximum_nominal_size
        
        self.exposure_condition = exposure_condition
        # slump (mm) used to adjust water content; reference table is for 50 mm
        self.slump_mm = float(slump_mm) if slump_mm is not None else None
        # fraction change per 25 mm (e.g. 0.03 == 3% change per 25 mm)
        self.slump_adjustment_pct_per_25mm = 0.03
        self.maximum_cement_content = maximum_cement_content #TODO : implement logic
        self.chemical_admixture = chemical_admixture
        if self.chemical_admixture is None:
            self.chemical_admixture_percentage = 0.0
        else:
            if chemical_admixture_percentage is None:
                self.chemical_admixture_percentage = float(chemical_admixture.default_percentage)
            else:
                self.chemical_admixture_percentage = float(chemical_admixture_percentage)


        mandatory_items = {Materials.CEMENT, Materials.COARSE_AGGREGATE, Materials.WATER, Materials.FINE_AGGREGATE}
        # Accept either a list[SpecificGravity] or a dict[Materials, SpecificGravity]
        if isinstance(specific_gravities, dict):
            sg_map = specific_gravities
        else:
            sg_map = {sg.material: sg for sg in specific_gravities}
        if not mandatory_items.issubset(set(sg_map.keys())):
            raise ValueError("Missing mandatory specific gravities.")
        self.specific_gravities = sg_map
        self.is_pumpable = is_pumpable
        
        self.coarse_aggregate_type = coarse_aggregate_type
        self.coarse_aggregate_water_absorption = coarse_aggregate_water_absorption
        self.coarse_aggregate_surface_moisture = coarse_aggregate_surface_moisture
        self.fine_aggregate_zone = fine_aggregate_zone
        self.fine_aggregate_surface_moisture = fine_aggregate_surface_moisture
        self.fine_aggregate_water_absorption = fine_aggregate_water_absorption

        self.mineral_admixture = mineral_admixture #TODO : implement logic
        # resolved percentage: user-provided overrides enum default
        if self.mineral_admixture is None:
            self.mineral_admixture_percentage = 0.0
        else:
            if mineral_admixture_percentage is None:
                self.mineral_admixture_percentage = float(mineral_admixture.default_percentage)
            else:
                self.mineral_admixture_percentage = float(mineral_admixture_percentage)
        

    def __calculate_water_cement_ratio_by_is456(self, reinforced: bool = True) -> float:
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
        self.initial_water_cement_ratio=wcr
        if self.chemical_admixture == ChemicalAdmixture.SUPERPLASTICIZER:
            wcr -= 0.05
        self.water_cement_ratio = float(wcr)

        if getattr(self, "_display_flag", False):
            print("\n" + "-"*60)
            print("Water / Cement Ratio (IS456 Table 5)")
            print("-"*60)
            print(f"Exposure condition : {self.exposure_condition.value}")
            print(f"Reinforced member  : {'Yes' if reinforced else 'No'}")
            print(f"Calculated W/C     : {self.water_cement_ratio:.3f}")
            print("-"*60)

        return self.water_cement_ratio

    def __calculate_water_content(self):
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
            adjusted_water *= (1 - self.chemical_admixture_percentage / 100)
        adjusted_water = round(adjusted_water)
        self.maximum_water_content = adjusted_water

        if getattr(self, "_display_flag", False):
            print("\n" + "-"*60)
            print("Water Content Determination")
            print("-"*60)
            print(f"Maximum nominal aggregate size : {self.maximum_nominal_size.value} mm")
            print(f"Base water content (50 mm slump): {base_water:.2f} kg/m^3")
            if self.slump_mm is not None:
                pct_change = (self.slump_adjustment_pct_per_25mm * 100.0)
                print(f"Slump provided                 : {self.slump_mm:.1f} mm")
                print(f"Adjustment per 25 mm           : {pct_change:.1f}%")
                print(f"Adjusted water content         : {adjusted_water:.2f} kg/m^3")
            if self.chemical_admixture == ChemicalAdmixture.SUPERPLASTICIZER:
                print(f"Superplasticizer used: water reduced by {self.chemical_admixture_percentage}%")
            print("-"*60)

        return adjusted_water


    def __calculate_target_mean_compressive_strength(self) -> float:
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

        if getattr(self, "_display_flag", False):
            print("\n" + "-"*60)
            print("Target Mean Compressive Strength")
            print("-"*60)
            print(f"Concrete grade (f_ck) : {self.concrete_grade.value} => {fck} N/mm^2")
            print(f"Standard deviation    : {s:.2f} N/mm^2")
            print(f"Target mean strength  : {target_mean:.2f} N/mm^2")
            print("-"*60)

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

        if getattr(self, "_display_flag", False):
            print("\n" + "-"*60)
            print("Cement Content Calculation")
            print("-"*60)
            print(f"Computed cement (water / w/c) : {cement_content:.2f} kg/m^3")
            print(f"Minimum cement for exposure   : {minimum_cement_content:.2f} kg/m^3")
            print(f"Final cement content selected : {self.minimum_cement_content:.2f} kg/m^3")
            print("-"*60)

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
            decrease = abs(round((0.5 - self.water_cement_ratio) / 0.05))
            self.coarse_aggregate_proportion = float(prop) + decrease * 0.01
        else:
            increase = abs(round((self.water_cement_ratio - 0.5) / 0.05))
            self.coarse_aggregate_proportion = float(prop) - increase * 0.01
        if self.is_pumpable:
            self.coarse_aggregate_proportion = round(self.coarse_aggregate_proportion * 0.9, 2)
        
        fine_aggregate_proportion = 1 - self.coarse_aggregate_proportion
        self.fine_aggregate_proportion = float(fine_aggregate_proportion)

        if getattr(self, "_display_flag", False):
            print("\n" + "-"*60)
            print("Aggregate Proportions (by volume)")
            print("-"*60)
            print(f"Fine aggregate zone            : {self.fine_aggregate_zone.value}")
            print(f"Nominal max size (mm)         : {self.maximum_nominal_size.value}")
            print(f"Base coarse proportion (table) : {prop:.3f}")
            print(f"W/C ratio                      : {self.water_cement_ratio:.3f}")
            print(f"Adjusted coarse proportion     : {self.coarse_aggregate_proportion:.3f}")
            if self.is_pumpable:
                print("Pumpable mix adjustment applied: coarse proportion reduced by 10%")
            print(f"Fine aggregate proportion      : {self.fine_aggregate_proportion:.3f}")
            print("-"*60)

        return self.coarse_aggregate_proportion, self.fine_aggregate_proportion

    def calculate_volume_based_on_mass_and_specific_gravity(self,mass,specific_gravity,round_value=3):
        """Calculate the volume based on mass and specific gravity.

        Args:
            mass (float): The mass of the material.
            specific_gravity (float): The specific gravity of the material.
            round_value (int): The number of decimal places to round the result.

        Returns:
            float: The volume of the material.
        """        
        volume = (mass / specific_gravity) * (1/1000)

        if getattr(self, "_display_flag", False):
            print(f"Volume from mass {mass:.2f} kg and SG {specific_gravity:.3f} -> {volume:.4f} m^3")

        return round(volume, round_value)

    def __get_specific_gravity(self, material: Materials) -> float:
        """Return the numeric specific gravity for a given material (raises if missing)."""
        sg = self.specific_gravities.get(material)
        if sg is None:
            raise ValueError(f"specific gravity for {material} not provided")
        return float(sg.value)

    def compute_mix_design(self, display_result: bool = False):
        """Compute the concrete mix design based on IS 456 and IS 10262.

        Args:
            display_result (bool, optional): Whether to display the calculation results. Defaults to False.

        Returns:
            dict: A dictionary containing the mix design parameters.
        """        
        self._display_flag = bool(display_result)
        if self._display_flag:
            print("\n" + "="*60)
            print("Concrete Mix Design - Calculation Summary")
            print("="*60)

        target_mean_strength = self.__calculate_target_mean_compressive_strength()
        water_cement_ratio = self.__calculate_water_cement_ratio_by_is456()
        water_content = self.__calculate_water_content()
        cement_content = self.__calculate_cement_content(water_cement_ratio, water_content)
        coarse_aggregate_proportion, fine_aggregate_proportion = self.__calculate_aggregate_content()

        volume_of_concrete=1
        volume_of_cement = self.calculate_volume_based_on_mass_and_specific_gravity(
            cement_content, self.__get_specific_gravity(Materials.CEMENT)
        )
        volume_of_water = self.calculate_volume_based_on_mass_and_specific_gravity(
            water_content, self.__get_specific_gravity(Materials.WATER)
        )
        # admixture content is percentage of cement content (use resolved percentage)
        self.admixture_content = cement_content * 0.02
        volume_of_admixture = self.calculate_volume_based_on_mass_and_specific_gravity(
            self.admixture_content, self.__get_specific_gravity(Materials.ADMIXTURE)
        )
        volume_of_all_in_aggregate=1-volume_of_cement - volume_of_water - volume_of_admixture

        self.coarse_aggregate_content = volume_of_all_in_aggregate * coarse_aggregate_proportion \
                                    * self.__get_specific_gravity(Materials.COARSE_AGGREGATE) * 1000
        self.fine_aggregate_content = volume_of_all_in_aggregate * fine_aggregate_proportion \
                                    * self.__get_specific_gravity(Materials.FINE_AGGREGATE) * 1000

        coarse_aggregate_water_absorption = self.coarse_aggregate_content * self.coarse_aggregate_water_absorption * 0.01
        fine_aggregate_water_absorption = self.fine_aggregate_content * self.fine_aggregate_water_absorption * 0.01
        coarse_aggregate_surface_moisture = self.coarse_aggregate_content * self.coarse_aggregate_surface_moisture * 0.01
        fine_aggregate_surface_moisture = self.fine_aggregate_content * self.fine_aggregate_surface_moisture * 0.01
        free_water_after_correction = water_content + coarse_aggregate_water_absorption + fine_aggregate_water_absorption - coarse_aggregate_surface_moisture - fine_aggregate_surface_moisture
        self.aggregate_absorbed_water = {"coarse": coarse_aggregate_water_absorption, "fine": fine_aggregate_water_absorption}
        self.aggregate_surface_moisture = {"coarse": coarse_aggregate_surface_moisture, "fine": fine_aggregate_surface_moisture}
        self.free_water_after_correction = float(free_water_after_correction)
        volume_of_free_water = self.calculate_volume_based_on_mass_and_specific_gravity(
            free_water_after_correction, self.__get_specific_gravity(Materials.WATER)
        )
        self.volume_of_free_water = float(volume_of_free_water)
        self.coarse_aggregate_volume = self.calculate_volume_based_on_mass_and_specific_gravity(
            self.coarse_aggregate_content, self.__get_specific_gravity(Materials.COARSE_AGGREGATE)
        )
        self.fine_aggregate_volume = self.calculate_volume_based_on_mass_and_specific_gravity(
            self.fine_aggregate_content, self.__get_specific_gravity(Materials.FINE_AGGREGATE)
        )

        if self._display_flag:
            print("\n" + "-"*60)
            print("Final Mix Quantities (per m^3 of concrete)")
            print("-"*60)
            print(f"{'Component':<20} | {'Mass (kg/m^3)':>15} | {'Volume (m^3)':>12}")
            print("-"*60)
            # volumes were calculated earlier
            print(f"{'Cement':<20} | {cement_content:15.2f} | {volume_of_cement:12.4f}")
            print(f"{'Water':<20} | {water_content:15.2f} | {volume_of_water:12.4f}")
            print(f"{'Admixture':<20} | {self.admixture_content:15.2f} | {volume_of_admixture:12.4f}")
            print(f"{'Coarse aggregate':<20} | {self.coarse_aggregate_content:15.2f} | {self.coarse_aggregate_volume:12.4f}")
            print(f"{'Fine aggregate':<20} | {self.fine_aggregate_content:15.2f} | {self.fine_aggregate_volume:12.4f}")
            print("-"*60)
            # reference only: free water after absorption/surface moisture corrections
            print(f"After absorption and surface moisture adjustments, free water available: "
                  f"{self.free_water_after_correction:.2f} kg "
                  f"({self.volume_of_free_water:.4f} m^3)")
            # additional reference: aggregate absorbed water and surface moisture (kg)
            print(f"Coarse aggregate absorbed water : {coarse_aggregate_water_absorption:.2f} kg")
            print(f"Fine   aggregate absorbed water : {fine_aggregate_water_absorption:.2f} kg")
            print(f"Coarse aggregate surface moisture: {coarse_aggregate_surface_moisture:.2f} kg")
            print(f"Fine   aggregate surface moisture: {fine_aggregate_surface_moisture:.2f} kg")
            print("-"*60)

        # clear display flag
        self._display_flag = False

        
        return {
            "summary": {
                "target_mean_strength_N_per_mm2": "self.target_mean_compressive_strength", 
                "water_cement_ratio": "self.water_cement_ratio"
            },
            "mix_per_m3": {
                "components": {
                    "cement": {
                        "mass_kg": cement_content,
                        "volume_m3": volume_of_cement,
                        "specific_gravity": self.__get_specific_gravity(Materials.CEMENT)
                    },
                    "water": {
                        "mass_kg": water_content,
                        "volume_m3": volume_of_water,
                        "specific_gravity": self.__get_specific_gravity(Materials.WATER)
                    },
                    "admixture": {
                        "mass_kg": self.admixture_content,
                        "volume_m3": volume_of_admixture,
                        "specific_gravity": self.__get_specific_gravity(Materials.ADMIXTURE),
                        "type": getattr(self.chemical_admixture, "name", None)
                    },
                    "coarse_aggregate": {
                        "mass_kg": self.coarse_aggregate_content,
                        "volume_m3": self.coarse_aggregate_volume,
                        "specific_gravity": self.__get_specific_gravity(Materials.COARSE_AGGREGATE),
                        "volume_proportion": self.coarse_aggregate_proportion
                    },
                    "fine_aggregate": {
                        "mass_kg": self.fine_aggregate_content,
                        "volume_m3": self.fine_aggregate_volume,
                        "specific_gravity": self.__get_specific_gravity(Materials.FINE_AGGREGATE),
                        "volume_proportion": self.fine_aggregate_proportion
                    }
                },
                "total_concrete_volume_m3": 1.0
            },
            "aggregate_adjustments_kg": {
                "coarse_absorbed_water": self.aggregate_absorbed_water['coarse'],
                "fine_absorbed_water": self.aggregate_absorbed_water['fine'],
                "coarse_surface_moisture": self.aggregate_surface_moisture['coarse'],
                "fine_surface_moisture": self.aggregate_surface_moisture['fine'],
                "free_water_after_correction": self.free_water_after_correction
            },
            "provenance": {
                "maximum_nominal_size_mm": self.maximum_nominal_size.value,
                "fine_aggregate_zone": self.fine_aggregate_zone.value,
                "is_pumpable": self.is_pumpable,
                "slump_mm": self.slump_mm,
                "chemical_admixture": getattr(self.chemical_admixture, "value", None),
                "chemical_admixture_percentage": self.chemical_admixture_percentage,
                "mineral_admixture": getattr(self.mineral_admixture, "value", None),
                "mineral_admixture_percentage": self.mineral_admixture_percentage
            }
        }

