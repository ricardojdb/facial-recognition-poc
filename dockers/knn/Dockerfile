# Use pytorch with cuda to get GPU support
FROM python:3.6.8-slim

LABEL Name="facial-recognition-poc" Version="0.0.1" maintainer="rjoseb11@gmail.com"\
      run="docker run --name=knn-service --link=vggface-service --rm -dit -v <PATH>:/app -p 7000:7000 knn"

# Create app folder
RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app

# Local directory as a volume
VOLUME /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port available to the world outside this container
EXPOSE 7000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]