# Use the specified Python slim-buster image
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy all local files into the /app directory in the container
COPY . /app

# Install necessary system packages and then clean up apt cache
# - `ca-certificates`: Essential for apt to trust HTTPS connections to repositories.
# - `curl`: Often useful for downloading files, though not strictly needed for apt itself.
# - `--no-install-recommends`: Prevents installation of recommended packages not strictly
#   required, helping to keep the image size small.
# - `rm -rf /var/lib/apt/lists/*`: Cleans up the apt cache after installation,
#   reducing the final image size significantly.
RUN apt update -y && \
    apt install -y --no-install-recommends ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*


# Install Python dependencies from requirements.txt
# This includes `awscli` if it's listed in your requirements.txt.
# It's generally best practice to install `awscli` via pip in a Python image.
RUN pip install -r requirements.txt

# Command to run when the container starts
CMD ["python3", "app.py"]
