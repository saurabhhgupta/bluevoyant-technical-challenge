#!/bin/bash

# Execute with sudo

s_DOCKER_IMAGE_NAME="bluevoyant_challenge_saurabh"

printf "Stopping old image %s\n" "${s_DOCKER_IMAGE_NAME}"
sudo docker stop "${s_DOCKER_IMAGE_NAME}"

printf "Removing old image %s\n" "${s_DOCKER_IMAGE_NAME}"
sudo docker rm "${s_DOCKER_IMAGE_NAME}"

printf "Creating Docker image %s\n" "${s_DOCKER_IMAGE_NAME}"
sudo docker build -t ${s_DOCKER_IMAGE_NAME} . --no-cache

i_EXIT_CODE=$?
if [ $i_EXIT_CODE -ne 0 ]; then
    printf "ERROR: Exit code %s\n" ${i_EXIT_CODE}
    exit
fi

echo "Ready to run ${s_DOCKER_IMAGE_NAME} Docker container"
echo "To run, type: sudo docker run -d -p 3306:3306 --name ${s_DOCKER_IMAGE_NAME} ${s_DOCKER_IMAGE_NAME}"
echo "or, use docker_run.sh"
echo
echo "Debug running Docker:"
echo "docker exec -it ${s_DOCKER_IMAGE_NAME} /bin/bash"
echo
echo "Running Docker container ${s_DOCKER_IMAGE_NAME}..."
docker run --env-file $1 -d -p 3306:3306 --name ${s_DOCKER_IMAGE_NAME} ${s_DOCKER_IMAGE_NAME}
echo
docker exec -it ${s_DOCKER_IMAGE_NAME} /bin/bash
