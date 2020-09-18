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
        columns=[
            (
                "subject.label", 
                "Subject"
            ),
            (
                "file.info.tbi-extractor.annotations.epidural_hemorrhage",
                "Epidural Hemorrhage"
            ),
            (
                "file.info.tbi-extractor.annotations.subdural_hemorrhage",
                "Subdural Hemorrhage"
            ),
            (
                "file.info.tbi-extractor.annotations.subarachnoid_hemorrhage",
                "Subarachnoid Hemorrhage"
            ),
            (
                "file.info.tbi-extractor.annotations.intraparenchymal_hemorrage",
                "Intraparenchymal Hemorrage"
            ),
            (
                "file.info.tbi-extractor.annotations.intraventricular_hemorrhage",
                "Intraventricular Hemorrhage"
            ),
            (
                "file.info.tbi-extractor.annotations.hemorrhage", 
                "Hemorrhage (NOS)"
            ),
            (
                "file.info.tbi-extractor.annotations.fluid",
                "Extraaxial Fluid Collection"
            ),
            (
                "file.info.tbi-extractor.annotations.skull_fracture",
                "Skull Fracture"
            ),
            (
                "file.info.tbi-extractor.annotations.facial_fracture", 
                "Facial Fracture"
            ),
            (
                "file.info.tbi-extractor.annotations.aneurysm", 
                "Aneurysm"
            ),
            (
                "file.info.tbi-extractor.annotations.herniation", 
                "Herniation"
            ),
            (
                "file.info.tbi-extractor.annotations.swelling", 
                "Swelling"
            ),
            (
                "file.info.tbi-extractor.annotations.mass_effect", 
                "Mass Effect"
            ),
            (
                "file.info.tbi-extractor.annotations.midline_shift", 
                "Midline Shift"
            ),
            (
                "file.info.tbi-extractor.annotations.cistern", 
                "Cisterns"
            ),
            (
                "file.info.tbi-extractor.annotations.contusion", 
                "Contustion"
            ),
            (
                "file.info.tbi-extractor.annotations.hyperdensities", 
                "Hyperdensities"
            ),
            (
                "file.info.tbi-extractor.annotations.hypodensities", 
                "Hypodensities"
            ),
            (
                "file.info.tbi-extractor.annotations.microhemorrhage", 
                "Microhemorrhage"
            ),
            (
                "file.info.tbi-extractor.annotations.diffuse_axonal",
                "Diffuse Axonal Injury",
            ),
            (
                "file.info.tbi-extractor.annotations.ischemia", 
                "Ischemia"
            ),
            (
                "file.info.tbi-extractor.annotations.anoxic", 
                "Anoxia"
            ),
            (
                "file.info.tbi-extractor.annotations.atrophy", 
                "Atrophy"
            ),
            (
                "file.info.tbi-extractor.annotations.hydrocephalus", 
                "Hydrocephalus"
            ),
            (
                "file.info.tbi-extractor.annotations.pneumocephalus", 
                "Pneumocephalus"
            ),
            (
                "file.info.tbi-extractor.annotations.intracranial_pathology",
                "Intracranial Pathology",
            )
        ],
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
