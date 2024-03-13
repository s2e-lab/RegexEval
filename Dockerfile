# Use the continuumio/anaconda3 base image
FROM continuumio/anaconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the ReDos_Benchmarking directory into the container at /app
COPY ReDos_Benchmarking /app

# Install dependencies
RUN pip install datasets && \
    #conda install -c huggingface -c conda-forge datasets && \
    pip install tqdm && \
    apt-get update && \
    apt-get -y install gcc mono-mcs python3-dev

# Specify the command to run on container start
CMD ["python", "-c", "from datasets import load_dataset"]

