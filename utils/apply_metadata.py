"""Functions to collate and apply metadata."""

import logging
import os

import flywheel


log = logging.getLogger(__name__)


def run(
    df,
    report_file_acquisition_id,
    report_file_name,
    scan_file_acquisition_id,
    scan_file_name,
    include_targets,
    analysis_id,
):
    """Collate tbiExtractor annotations and apply as metadata to scan file.

    Args:
        df (pandas.core.frame.DataFrame): dataframe containing each
            identified target phrase with its associated modifer phrase,
            if indicated in arguments; default includes the target group
            and modifier group.

        report_file_acquisition_id (str): Flywheel ID for the acquisition
            container containing the report file.

        report_file_name (str): Flywheel file name for the report file.

        scan_file_acquisition_id (str): Flywheel ID for the acquisition
            container containing the scan file.

        scan_file_name (str): Flywheel file name for the scan file.

        include_targets (list): Set of lexical targets used as input
            to tbiExtractor.

        analysis_id (str): Flywheel ID for the analysis
            container or a tag to give in the metadata output.

    Returns:
        None.

    """
    API_KEY = os.environ.get("FW_KEY")
    fw = flywheel.Client(API_KEY)

    log.info("Collating and constructing metadata.")

    # Store the report_file file ID
    acq = fw.get_acquisition(report_file_acquisition_id)
    for file in acq.files:
        if file.name == report_file_name:
            report_file_id = file.id

    # Collate annotations into metadata format
    annotations = collate_annotations(df, include_targets)

    # Construct metadata dictionary
    metadata = {
        "attributes": {
            "radiology report file ID": report_file_id,
            "analysis ID": analysis_id,
            "lexical targets assessed": include_targets,
        },
        "annotations": annotations,
    }

    # Apply metadata to corresponding scan file
    acq = fw.get_acquisition(scan_file_acquisition_id)
    file = acq.get_file(scan_file_name)
    file.update_info({"tbi-extractor": metadata})
    log.info(f"tbi-extractor metadata applied to {scan_file_name}.")


def collate_annotations(df, include_targets):
    """Collate annotations for each lexical target.

    Args:
        df (pandas.core.frame.DataFrame): dataframe containing each
            identified target phrase with its associated modifer phrase,
            if indicated in arguments; default includes the target group
            and modifier group.

        include_targets (list): Set of lexical targets used as input
            to tbiExtractor.

    Returns:
        annotations (dict): For each lexical target, store the annotation,
            and if applicable, store the derivations, which include the
            lexical target phrase and lexical modifier phrase.

    """
    annotations = {}
    for target in include_targets:

        # Find the target in the dataframe
        index = df.index[df["target_group"] == target]

        # Extract the associated annotation for the target
        annotation = df.loc[index, "modifier_group"].item()
        target_annotation = {target: annotation}

        # Collate target derivations
        annotations.update(target_annotation)

    if ("target_phrase" in df.columns) and ("modifier_phrase" in df.columns):
        derivations = collate_derivations(df, include_targets, True, True)
        annotations.update({"_derivations": derivations})
        log.info("tbiExtractor derivations will be included in metadata.")

    elif "target_phrase" in df.columns:
        derivations = collate_derivations(df, include_targets, True, False)
        annotations.update({"_derivations": derivations})
        log.info("tbiExtractor derivations will be included in metadata.")

    elif "modifier_phrase" in df.columns:
        derivations = collate_derivations(df, include_targets, False, True)
        annotations.update({"_derivations": derivations})
        log.info("tbiExtractor derivations will be included in metadata.")

    return annotations


def collate_derivations(
    df,
    include_targets,
    save_target_phrases=False,
    save_modifier_phrases=False,
):
    """Collate derivations for each lexical target.

    Args:
        df (pandas.core.frame.DataFrame): dataframe containing each
            identified target phrase with its associated modifer phrase,
            if indicated in arguments; default includes the target group
            and modifier group.

        include_targets (list): Set of lexical targets used as input
            to tbiExtractor.

        save_target_phrases (bool): If True, save the lexical target phrases
            identified in the report for the resulting annotation in metadata.
            Default is False.

        save_modifier_phrases (bool): If True, save the lexical modifier phrases
            identified in the report for the resulting annotation in metadata.
            Default is False.

    Returns:
        derivations (dict): For each lexical target, store the annotation,
            and if applicable, the target phrase and/or modifier phrase.

    """
    derivations = {}
    for target in include_targets:

        target_derivations = {}

        # Find the target in the dataframe
        index = df.index[df["target_group"] == target]

        # Extract the associated derivations for each target
        annotation = df.loc[index, "modifier_group"].item()
        target_derivations.update({"annotation": annotation})

        if save_target_phrases:
            target_phrase = df.loc[index, "target_phrase"].item()
            target_derivations.update({"target_phrase": target_phrase})

        if save_modifier_phrases:
            modifier_phrase = df.loc[index, "modifier_phrase"].item()
            target_derivations.update({"modifier_phrase": modifier_phrase})

        # Collate target derivations
        derivations.update({target: target_derivations})

    return derivations
