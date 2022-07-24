FROM python:3-slim

LABEL maintainer="d-Rickyy-b <certleak@rico-j.de>"
LABEL site="https://github.com/d-Rickyy-b/certleak"

# Create bot & log directories
RUN mkdir -p /certleak/logs && mkdir -p /certleak/src

# Copy the source code to the container
COPY . /certleak/src

RUN pip3 install --upgrade --no-cache pip \
 && pip3 install --no-cache setuptools wheel \
 && cd /certleak/src && python3 /certleak/src/setup.py install \
 && rm -rf /certleak/src/build

WORKDIR /certleak

# Start the main file when the container is started
ENTRYPOINT ["python3", "/certleak/main.py"]
