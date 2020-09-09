import pandas as pd

from tbi_extractor import run_algorithm

TARGETS = [
    "aneurysm",
    "anoxic",
    "atrophy",
    "cistern",
    "contusion",
    "diffuse_axonal",
    "epidural_hemorrhage",
    "facial_fracture",
    "fluid",
    "gray_white_differentiation",
    "hemorrhage",
    "herniation",
    "hydrocephalus",
    "hyperdensities",
    "hypodensities",
    "intracranial_pathology",
    "intraparenchymal_hemorrage",
    "intraventricular_hemorrhage",
    "ischemia",
    "mass_effect",
    "microhemorrhage",
    "midline_shift",
    "pneumocephalus",
    "skull_fracture",
    "subarachnoid_hemorrhage",
    "subdural_hemorrhage",
    "swelling",
]


def test_AlgorithmFunction_AllInputsAccurate():

    gear_args = {
        "report_file": "tests/assets/report_one.txt",
        "include_targets": TARGETS,
        "save_target_phrases": True,
        "save_modifier_phrases": True,
    }

    df1 = run_algorithm.run(**gear_args)
    df2 = pd.read_csv("tests/assets/df_report_one.csv")

    assert df1.all().all() == df2.all().all()


def test_AlgorithmFunction_NoPhrasesAccurate():

    gear_args = {
        "report_file": "tests/assets/report_two.txt",
        "include_targets": TARGETS,
        "save_target_phrases": False,
        "save_modifier_phrases": False,
    }

    df1 = run_algorithm.run(**gear_args)
    df2 = pd.read_csv("tests/assets/df_report_two.csv")

    assert df1.all().all() == df2.all().all()
