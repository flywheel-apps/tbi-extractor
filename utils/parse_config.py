"""Function to parse gear config into gear args."""

import logging
import os
import pprint


log = logging.getLogger(__name__)


def generate_gear_args(gear_context, FLAG):
    """Generate gear arguments."""

    # Gather configured lexical targets
    configured_targets = {
        "aneurysm": gear_context.config["aneurysm"],
        "anoxic": gear_context.config["anoxic"],
        "atrophy": gear_context.config["atrophy"],
        "cistern": gear_context.config["cistern"],
        "contusion": gear_context.config["contusion"],
        "diffuse_axonal": gear_context.config["diffuse_axonal"],
        "epidural_hemorrhage": gear_context.config["epidural_hemorrhage"],
        "facial_fracture": gear_context.config["facial_fracture"],
        "fluid": gear_context.config["fluid"],
        "gray_white_differentiation": gear_context.config["gray_white_differentiation"],
        "hemorrhage": gear_context.config["hemorrhage"],
        "herniation": gear_context.config["herniation"],
        "hydrocephalus": gear_context.config["hydrocephalus"],
        "hyperdensities": gear_context.config["hyperdensities"],
        "hypodensities": gear_context.config["hypodensities"],
        "intracranial_pathology": gear_context.config["intracranial_pathology"],
        "intraparenchymal_hemorrage": gear_context.config["intraparenchymal_hemorrage"],
        "intraventricular_hemorrhage": gear_context.config["intraventricular_hemorrhage"],
        "ischemia": gear_context.config["ischemia"],
        "mass_effect": gear_context.config["mass_effect"],
        "microhemorrhage": gear_context.config["microhemorrhage"],
        "midline_shift": gear_context.config["midline_shift"],
        "pneumocephalus": gear_context.config["pneumocephalus"],
        "skull_fracture": gear_context.config["skull_fracture"],
        "subarachnoid_hemorrhage": gear_context.config["subarachnoid_hemorrhage"],
        "subdural_hemorrhage": gear_context.config["subdural_hemorrhage"],
        "swelling": gear_context.config["subdural_hemorrhage"],
    }

    # Construct lexical target list for algorithm
    include_targets = []
    for target, config in configured_targets.items():
        if config:
            include_targets.append(target)

    if include_targets == []:
        log.error("Must select at least one lexical target to be annotated. Exiting.")
        os.sys.exit(1)

    # Algorithm stage
    if FLAG == "algorithm":
        log.info("Preparing arguments for tbiExtractor algorithm.")

        # Check the radiology report file input
        gear_args = {
            "report_file": gear_context.get_input_path("radiology_report"),
            "include_targets": include_targets,
            "save_target_phrases": gear_context.config["save_target_phrases"],
            "save_modifier_phrases": gear_context.config["save_modifier_phrases"],
        }

    # Metadata stage
    elif FLAG == "metadata":
        log.info("Preparing arguments for tbi-extractor metadata.")

        if gear_context.destination["type"] == "analysis":
            analysis_id = gear_context.destination["id"]
        else:
            log.error("Gear destination has been altered. Exiting.")
            os.sys.exit(1)

        if (
            gear_context.get_input("radiology_report")["hierarchy"].get("type")
            == "acquisition"
        ):
            report_file_acquisition_id = gear_context.get_input("radiology_report")["hierarchy"].get("id")
        else:
            log.error("Gear hierarchy has been altered. Exiting.")
            os.sys.exit(1)

        if (
            gear_context.get_input("corresponding_scan")["hierarchy"].get("type")
            == "acquisition"
        ):
            scan_file_acquisition_id = gear_context.get_input("corresponding_scan")["hierarchy"].get("id")
        else:
            log.error("Gear hierarchy has been altered. Exiting.")
            os.sys.exit(1)

        gear_args = {
            "report_file_acquisition_id": report_file_acquisition_id,
            "report_file_name": gear_context.get_input("radiology_report")["location"].get("name"),
            "scan_file_acquisition_id": scan_file_acquisition_id,
            "scan_file_name": gear_context.get_input("corresponding_scan")["location"].get("name"),
            "include_targets": include_targets,
            "analysis_id": analysis_id,
        }

    # Set API key as environment variable
    os.environ["FLYWHEEL_API_KEY"] = f"{gear_context.get_input('api_key')['key']}"

    gear_args_formatted = pprint.pformat(gear_args)
    log.info(f"Prepared gear stage arguments: \n\n{gear_args_formatted}\n")

    return gear_args
