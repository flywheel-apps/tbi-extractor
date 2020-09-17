#!/usr/bin/env python3
"""Main script for tbi-extractor demo."""
import os

import populate_instance
import run_gear
import create_dataview


def main():

    # Populate Flywheel Instance with demo data
    API_KEY = os.environ.get("FW_KEY")
    print("Begin populating instance with demo data.")
    populate_instance.run(API_KEY)

    # Run tbi-extractor Gear on demo data
    print(
        "Finished populating instance. Will begin submitting tbi-extractor Gear jobs."
    )
    run_gear.run(API_KEY)
    print("Finished executing tbi-extractor Gear jobs.")

    # Create data view
    print("Creating Data View.")
    create_dataview.run(API_KEY)
    print(
        "Finished creating Data View. All jobs will need to be completed to see full results in Data View."
    )

    return 0


if __name__ == "__main__":

    exit_status = main()
    print("Demo script complete.")
