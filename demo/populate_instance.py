"""Populate a Flywheel Instance with demo data."""
import glob
import json

import flywheel


def run(API_KEY):
    """Orchestrate instance data population."""

    # Setup
    GROUP_ID = "tbi-extractor"
    GROUP_LABEL = "TBI Extractor Demo"
    PROJECT_LABEL = "tbi-extractor"
    fw = flywheel.Client(api_key=API_KEY)

    # Create group and project
    if fw.groups.find_first(f"label={GROUP_LABEL}"):
        GROUP_ID = fw.add_group(flywheel.Group(GROUP_ID, GROUP_LABEL))

    group = fw.get(GROUP_ID)

    if group.projects.find_first(f"label={PROJECT_LABEL}"):
        print(
            "tbi-extractor project exists. No attempts to establish coherence will be made."
        )
        project = group.projects.find_first(f"label={PROJECT_LABEL}")
    else:
        project = group.add_project(label=f"{PROJECT_LABEL}")

    # Populate instance with subjects, sessions, acquisitions, and files
    demo_subjects = glob.glob("data/*", recursive=True)
    for demo_subject in demo_subjects:

        # Create subject from list of demo data subjects
        SUBJECT_LABEL = demo_subject.split("/")[-1]
        if not project.subjects.find_first(f"label={SUBJECT_LABEL}"):
            subject = project.add_subject(label=SUBJECT_LABEL)
        else:
            subject = project.subjects.find_first(f"label={SUBJECT_LABEL}")

        # Create session and acquisition for the subject
        SESSION_LABEL = "ses-01"
        if not subject.sessions.find_first(f"label={SESSION_LABEL}"):
            session = subject.add_session(label=SESSION_LABEL)
        else:
            session = subject.sessions.find_first(f"label={SESSION_LABEL}")

        ACQUISITION_LABEL = "noncontrast-head-ct"
        if not session.acquisitions.find_first(f"label={ACQUISITION_LABEL}"):
            acquisition = session.add_acquisition(label=ACQUISITION_LABEL)
        else:
            acquisition = session.acquisitions.find_first(f"label={ACQUISITION_LABEL}")

        # Add files to acquisition for the subject
        files = glob.glob(demo_subject + "/*")
        for file in files:
            if not acquisition.get_file(file):

                if file.endswith(".zip"):
                    metadata = json.dumps({"type": "dicom"})
                    fw.upload_file_to_acquisition(
                        acquisition.id, file, metadata=metadata
                    )
                elif file.endswith(".nii.gz"):
                    metadata = json.dumps({"type": "nifti"})
                    fw.upload_file_to_acquisition(
                        acquisition.id, file, metadata=metadata
                    )
                else:
                    fw.upload_file_to_acquisition(acquisition.id, file)
