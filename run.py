#!/usr/bin/env python3
"""Main script for tbi-extractor gear."""

import os

import flywheel_gear_toolkit
from tbi_extractor import run_algorithm

from utils import parse_config
from utils import apply_metadata


def main(gear_context):
    """Orchestrate tbi-extractor gear."""
    log.info("Starting tbi-extractor gear.")

    # Prepare for algorithm
    gear_args = parse_config.generate_gear_args(gear_context, "algorithm")

    # Run tbiExtractor
    df = run_algorithm.run(**gear_args)

    if len(gear_args["include_targets"]) != len(df):
        log.error(
            "The number of input lexical targets does not match output as expected. Exiting."
        )
        os.sys.exit(1)

    # Apply metadata update
    gear_args = parse_config.generate_gear_args(gear_context, "metadata")
    apply_metadata.run(df, **gear_args)

    exit_status = 0
    return exit_status


if __name__ == "__main__":

    with flywheel_gear_toolkit.GearToolkitContext() as gear_context:
        log = gear_context.log
        exit_status = main(gear_context)

    log.info(f"Successful tbi-extractor gear execution with exit status {exit_status}.")
