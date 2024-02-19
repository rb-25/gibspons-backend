# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/gibspons/

# Copy the requirements file into the container at /usr/src/app/
COPY ./requirements.txt /usr/src/gibspons/

# Install any needed packages specified in requirements.txt
RUN apt-get update \
    && apt-get install -y libpq-dev \
    && pip install --no-cache-dir psycopg2 \
    && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app/
COPY . /usr/src/gibspons/

# Run database migrations and start the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]