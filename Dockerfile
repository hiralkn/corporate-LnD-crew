FROM python:3.11-slim

# Install system dependencies needed for native C++ compilation modules (ChromaDB requirement)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Copy your dependency rules first to optimize caching speeds
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all application code into the file architecture container
COPY . /code

# Enforce Python search paths to treat your 'src' layout folder as a system module core root
ENV PYTHONPATH=/code/src

# Expose standard Gradio cloud interface port
EXPOSE 7860

# Run the app engine module directly via the modified search path blueprint
CMD ["python", "-m", "engineering_team.app"]
