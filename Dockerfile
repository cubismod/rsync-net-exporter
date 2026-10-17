# Install uv
FROM python:3.15-slim@sha256:2da676046630d7bf14c6764ae1143dc7fa0377a53f94bf5a642f0b214aca5bce
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Change the working directory to the `app` directory
WORKDIR /app

# Copy the lockfile and `pyproject.toml` into the image
COPY uv.lock /app/uv.lock
COPY pyproject.toml /app/pyproject.toml

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy the project into the image
COPY . /app

# Sync the project
RUN uv sync --frozen

CMD [ "python", "rsync_net_exporter/foo.py" ]
