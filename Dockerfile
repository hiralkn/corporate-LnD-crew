FROM python:3.11-slim

# Install system dependencies needed for vector databases (ChromaDB)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Copy requirements and install them
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all application source code
COPY . .

# Expose the standard Gradio port (7860 is required by Hugging Face)
EXPOSE 7860

# Command to run your app module directly
CMD ["python", "-m", "src.engineering_team.app"]
