# Use an official Debian 12 "bookworm" as a base image.
FROM debian:bookworm-slim

# Add user that will be used in the container.
RUN useradd svjisuser

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gettext \
    curl \
    ca-certificates \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "svjisuser" user. This project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown svjisuser:svjisuser /app
RUN chown svjisuser:svjisuser /home

# Copy the source code of the project into the container.
COPY --chown=svjisuser:svjisuser ./svjis ./svjis
COPY --chown=svjisuser:svjisuser ./pyproject.toml .
COPY --chown=svjisuser:svjisuser ./uv.lock .

# Install uv.
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
 && cp /root/.local/bin/uv /bin/uv \
 && rm -Rf /root/.local

# Use user "svjisuser" to run the build commands below and the server itself.
USER svjisuser

# Install packages.
RUN uv sync --no-dev --group linux-server

# Collect static files.
RUN .venv/bin/python svjis/manage.py collectstatic --noinput --clear

# Compile messages

RUN .venv/bin/python svjis/manage.py compilemessages

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   SVJIS instance can be started with a simple "docker run" command.
CMD set -xe; .venv/bin/python svjis/python manage.py migrate --noinput; cd svjis && ../.venv/bin/gunicorn svjis.wsgi:application
