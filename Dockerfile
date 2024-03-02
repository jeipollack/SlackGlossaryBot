# Use Python 3.11.3 as the base image
FROM python:3.11.3

# Set environment variables
ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Update pip
RUN pip install --upgrade pip

# Set working directory
WORKDIR /opt/SlackGlossaryBot

# Copy the source code
COPY . .

# List the contents of the directory
RUN ls -l

# Install project dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev


# Set working directory
WORKDIR /opt/SlackGlossaryBot

# Default command
CMD ["sleep", "infinity"]


