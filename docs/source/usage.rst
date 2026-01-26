Usage
=====

Example: concrete mix design (Indian Standards)
-----------------------------------------------

The example below shows how to create a ConcreteMixDesign, compute the mix and print the results.

.. code-block:: python

    from civilutils.indian_standards.concrete import *
    from pprint import pprint

    design = ConcreteMixDesign(
        concrete_grade=ConcreteGrade.M40,
        maximum_nominal_size=MaximumNominalSize.SIZE_20,
        slump_mm=100.0,
        is_pumpable=True,
        exposure_condition=ExposureCondition.SEVERE,
        specific_gravities=[
            SpecificGravity(Materials.CEMENT, 3.16),
            SpecificGravity(Materials.FINE_AGGREGATE, 2.74),
            SpecificGravity(Materials.COARSE_AGGREGATE, 2.74),
            SpecificGravity(Materials.ADMIXTURE, 1.145),
            SpecificGravity(Materials.WATER, 1.00),
        ],
        chemical_admixture=ChemicalAdmixture.SUPERPLASTICIZER,
        chemical_admixture_percentage=29.0,
        coarse_aggregate_type=CoarseAggregateType.CRUSHED_ANGULAR,
        fine_aggregate_zone=FineAggregateZone.ZONE_I,
        fine_aggregate_water_absorption=0.1,
        coarse_aggregate_water_absorption=0.05
    )

    # The following call prints the computed mix when display_result=True:
    _ = design.compute_mix_design(display_result=True)

    # If you prefer to capture the result (no automatic printing), disable display_result:
    # result = design.compute_mix_design(display_result=False)
    # pprint(result)

Notes
-----
- Adjust input parameters to match your materials and site conditions.
- Use pprint(result) to inspect the returned structure when you capture the result.