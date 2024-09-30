#!/bin/bash

# Load environment variables from .env file (optional, adjust path if needed)
if [ -f ".env" ]; then
  source .env
fi


# Get project name from environment variable (error handling)
project_name=${PROJECT_NAME:-"unknown"}  # Default to "unknown" if not set
if [[ -z "$project_name" ]]; then
  echo "Error: Missing environment variable PROJECT_NAME"
  exit 1
fi


# Function to build Docker image
docker_build() {
  	image_tag="$project_name"_container
  	echo "Building Docker image: $image_tag"
  	docker build -t "$image_tag" . || {
    	echo "Error: Failed to build Docker image"
    	exit 1
  	}
}

# Function to run Docker container
docker_run() {
  	port=${1:-8000}  # Default port is 8000
  	image_tag="$project_name"_container
  	echo "Running Docker container: $image_tag (port: $port)"
  	docker run -p "$port:8000" "$image_tag" || {
    	echo "Error: Failed to run Docker container"
    	exit 1
  	}
}

# Function to stop Docker container
docker_stop() {
	image_tag="$project_name"_container
  	echo "Stopping Docker container: $image_tag"
  	docker stop "$image_tag" || true  # Ignore errors if container not running
}

# Function to restart Docker container
docker_restart() {
    docker_stop
    docker_run
}

# Function to remove Docker container
docker_remove() {
	image_tag="$project_name"_container
  	echo "Removing Docker container: $image_tag"
  	docker rm "$image_tag" || true  # Ignore errors if container not removed
}


# Function to delete Docker image
docker_image_delete() {
  image_tag="$project_name"_container
  echo "Deleting Docker image: $image_tag"
  docker rmi "$image_tag" || {
    echo "Error: Failed to delete Docker image"
    exit 1
  }
}


# Main script
case "$1" in
    build) docker_build ;;
    run) docker_run ;;
    stop) docker_stop ;;
    restart) docker_restart ;;
    remove) docker_remove ;;
    delete) docker_image_delete ;;
    *)
        echo "Usage: $0 {build|run|stop|restart|remove}" >&2
        exit 1
        ;;
esac
