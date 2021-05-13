FROM python:3-slim

LABEL maintainer="d-Rickyy-b <certleak@rico-j.de>"
LABEL site="https://github.com/d-Rickyy-b/certleak"

# Create bot & log directories
RUN mkdir -p /certleak/logs
WORKDIR /certleak

# Copy the source code to the container
COPY . /certleak

RUN pip3 install --no-cache -r /certleak/requirements.txt

# Start the main file when the container is started
ENTRYPOINT ["python3", "main.py"]
