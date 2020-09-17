"""Create a Data View for tbi-extractor results."""
import flywheel


def run(API_KEY):
    """Orchestrate data view creation."""

    # Setup
    PROJECT_LABEL = "tbi-extractor"
    fw = flywheel.Client(api_key=API_KEY)

    # Load the project
    project = fw.projects.find_first(f"label={PROJECT_LABEL}")

    # Create the data view structure
    view = fw.View(
        label="tbi-extractor Results",
        columns=["subject.label",
                 "file.info.tbi-extractor.annotations.aneurysm",
                 "file.info.tbi-extractor.annotations.anoxic",
                 "file.info.tbi-extractor.annotations.atrophy",
                 "file.info.tbi-extractor.annotations.cistern",
                 "file.info.tbi-extractor.annotations.contusion",
                 "file.info.tbi-extractor.annotations.diffuse_axonal",
                 "file.info.tbi-extractor.annotations.epidural_hemorrhage",
                 "file.info.tbi-extractor.annotations.facial_fracture",
                 "file.info.tbi-extractor.annotations.fluid",
                 "file.info.tbi-extractor.annotations.gray_white_differentiation",
                 "file.info.tbi-extractor.annotations.hemorrhage",
                 "file.info.tbi-extractor.annotations.herniation",
                 "file.info.tbi-extractor.annotations.hydrocephalus",
                 "file.info.tbi-extractor.annotations.hyperdensities",
                 "file.info.tbi-extractor.annotations.hypodensities",
                 "file.info.tbi-extractor.annotations.intracranial_pathology",
                 "file.info.tbi-extractor.annotations.intraparenchymal_hemorrage",
                 "file.info.tbi-extractor.annotations.intraventricular_hemorrhage",
                 "file.info.tbi-extractor.annotations.ischemia",
                 "file.info.tbi-extractor.annotations.mass_effect",
                 "file.info.tbi-extractor.annotations.microhemorrhage",
                 "file.info.tbi-extractor.annotations.midline_shift",
                 "file.info.tbi-extractor.annotations.pneumocephalus",
                 "file.info.tbi-extractor.annotations.skull_fracture",
                 "file.info.tbi-extractor.annotations.subarachnoid_hemorrhage",
                 "file.info.tbi-extractor.annotations.subdural_hemorrhage",
                 "file.info.tbi-extractor.annotations.swelling"],
        container="acquisition",
        filename="noncontrast-head-ct.*",
    )

    # Add the data view to the project
    view_id = fw.add_view(project.id, view)

    # Print a link to the data view created
    url_prefix = ":".join(fw.get_config().site.api_url.split(":")[:2])
    result_url = f"{url_prefix}/#/projects/{project.id}/dataViews/{view_id}"
    newline = "\n\n"
    print(f"Link to Data View of tbi-extractor results: {newline}{result_url}")
