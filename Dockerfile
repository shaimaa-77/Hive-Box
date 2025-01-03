#base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app
# Install Poetry
RUN pip install --no-cache-dir poetry
#copy all file 
COPY . /app
# Install the Python dependencies
RUN poetry install --no-root

# Set the default command to run your app
CMD [ "poetry","run","python3","setup.py" ]