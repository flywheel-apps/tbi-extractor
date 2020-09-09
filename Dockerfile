# tbi-extractor gear
FROM python:3.6-slim-stretch
MAINTAINER Flywheel <support@flywheel.io>

# Python setup
RUN apt-get update && apt-get install --no-install-recommends -y python3-dev gcc build-essential
RUN python -m pip install --no-cache-dir https://github.com/margaretmahan/tbiExtractor/archive/0.2.0.tar.gz
RUN python -m spacy download en
RUN pip install flywheel-gear-toolkit

# Flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}
WORKDIR ${FLYWHEEL}

# Gear setup
COPY manifest.json ${FLYWHEEL}/manifest.json
ADD utils ${FLYWHEEL}/utils
COPY run.py ${FLYWHEEL}/run.py
RUN chmod +x ${FLYWHEEL}/run.py
