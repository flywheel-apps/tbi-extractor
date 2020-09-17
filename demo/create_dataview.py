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
        columns=["subject.label", "file.info.tbi-extractor.annotations.fluid"],
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
