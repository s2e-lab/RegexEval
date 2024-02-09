# Use the continuumio/anaconda3 base image
FROM continuumio/anaconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the RegexEval_Docker directory into the container at /app
COPY ReDos_Benchmarking /app

# Set PATH environment variable to include directory containing WebDriver binaries
#ENV PATH="/usr/local/bin:${PATH}"

# Dependencies
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    apt-get update && apt-get install -y unzip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /DatasetCollection

RUN pip install selenium==4.3.0

# Specify the command to run on container start
#CMD ["python", "Data_Collection.py"]

