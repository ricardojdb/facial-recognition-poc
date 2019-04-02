# Use pytorch with cuda to get GPU support
# docker build -t vggface .
# if GPU :0.4_cuda9_cudnn7
FROM pytorch/pytorch

# LABEL 'docker run --name=vggface-service --rm --dt -v /home/deepai/Documents/projects/facial-recognition-poc/dockers/vggface:/app -p 7001:7000 vggface:gpu'

# Create app folder
RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Local directory as a volume
VOLUME /home/deepai/Documents/projects/facial-recognition-poc/dockers/vggface:/app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port available to the world outside this container
EXPOSE 7000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]