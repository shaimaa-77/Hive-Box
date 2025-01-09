#base image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000
# Set the working directory in the container
WORKDIR /app

#copy requirement.txt 
COPY ./requirements.txt /app/requirements.txt


# Install dependances
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
#copy all file 
COPY . /app
#add user for non root usage
RUN adduser --disabled-password --gecos '' appuser chown -R appuser:appuser /app
USER appuser
# Expose the port
EXPOSE $PORT
# Set the default command to run your app
CMD ["uvicorn", "main:app" ,"--host","0.0.0.0","--port","8000"]
