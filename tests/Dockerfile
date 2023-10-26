# version Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the local script files into the container at /usr/src/app
COPY --chmod=555 SetupEnv.sh run_test.sh ./

# Install any needed packages specified in SetupEnv.sh
RUN ./SetupEnv.sh

COPY test_files/* ./
# Run run_test.sh when the container launches
ENTRYPOINT ["./run_test.sh"]
