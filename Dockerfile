FROM python:3.11-slim

# Install system dependencies needed for native C++ modules
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the official high-speed uv binary directly into our container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

# Copy and install sanitized requirements using uv (avoids RAM limits and wheel failures)
COPY ./requirements.txt /code/requirements.txt
RUN uv pip install --system --no-cache -r /code/requirements.txt

# Copy all application code into the file architecture container
COPY . /code

# Enforce Python search paths to treat your 'src' layout folder as a system module core root
ENV PYTHONPATH=/code/src

# Expose standard Gradio cloud interface port
EXPOSE 7860

# Run the app engine module directly via the modified search path blueprint
CMD ["python", "-m", "engineering_team.app"]
