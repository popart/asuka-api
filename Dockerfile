# Set base image (host OS)
FROM python:3.12.3-bookworm

# Set the working directory in the container
WORKDIR /app

# Install poetry
RUN apt update
RUN apt install pipx -y
RUN pipx install poetry
ENV PATH=/root/.local/bin:$PATH

# Install any dependencies
COPY ./pyproject.toml /app
COPY ./poetry.lock /app
RUN poetry install

# Copy the content of the local src directory to the working directory
COPY ./src /app

# Specify the command to run on container start
CMD [ "python", "./app.py" ]

# Make port 5000 available to the world outside this container
EXPOSE 5000/tcp

# Run app.py when the container launches
CMD ["poetry", "run", "python", "app.py"]
