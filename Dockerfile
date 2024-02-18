# Use Python 3.11.3 as the base image
FROM python:3.11.3

# Set environment variables
ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Update pip
RUN pip install --upgrade pip

# Set working directory
WORKDIR /opt/SlackGlossary

# Copy only the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy the source code
COPY . .

# Set working directory
WORKDIR /opt/SlackGlossary

# Default command
CMD ["sleep", "infinity"]


