# Requirements

The Flywheel SDK must be in the Python path you use to execute the demo script.
You must have the appropriate Flywheel permissions to write across the Flywheel hierarchy.

# Recommended steps to demonstrate tbi-extractor Gear

1. Download the repository
2. Build the docker image
    `docker build -t tbi_extractor:demo ./`
3. Run the docker image
    `docker run -it -v <PATH-TO-DEMO-DIRECTORY>/demo:/flywheel/v0/demo --entrypoint /bin/bash tbi_extractor:demo`
4. Inside the docker image
    `cd demo`
    `export FW_KEY=<FLYWHEEL-API-KEY>`
    `python3 demo.py`
   
When finished, a link will be desplayed to the Data View with tbi-extractor Gear results from the demo data.

