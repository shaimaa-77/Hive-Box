#base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

#copy requirement.txt 
COPY ./requirements.txt /app/requirements.txt


# Install dependances
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
#copy all file 
COPY . /app

# Set the default command to run your app
CMD ["poetry", "run","python3", "app_version.py" ]
