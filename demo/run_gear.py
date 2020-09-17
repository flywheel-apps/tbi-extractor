"""Run tbi-extractor Gear on demo data."""
import flywheel


def run(API_KEY):
    """Orchestrate gear run."""

    # Setup
    PROJECT_LABEL = "tbi-extractor"
    fw = flywheel.Client(api_key=API_KEY)

    # Load the project
    project = fw.projects.find_first(f"label={PROJECT_LABEL}")

    # Load the Gear
    tbi_extractor_gear = fw.lookup("gears/tbi-extractor")

    # For each session in the project, find the inputs and run tbi-extractor
    for session in project.sessions.iter():

        # Iterate over sessions acquisition
        for i, acq in enumerate(session.acquisitions.iter()):

            # Assuming demo data reflected in Flywheel, meaning there are two files per acquisition
            if len(acq.files) == 2:

                for file in acq.files:
                    if file.type == "text":
                        radiology_report = file
                    if (file.type == "dicom") or (file.type == "nifti"):
                        corresponding_scan = file

                inputs = {
                    "radiology_report": radiology_report,
                    "corresponding_scan": corresponding_scan,
                }

                config = {"save_target_phrases": True, "save_modifier_phrases": True}

                tbi_extractor_gear.run(
                    analysis_label="Demo",
                    config=config,
                    inputs=inputs,
                    destination=session,
                )
