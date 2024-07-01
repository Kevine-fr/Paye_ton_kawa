pipeline {
    agent any

    environment {
        CONTAINER_NAME = "Client"
        IMAGE_NAME = "client-img"
    }

    stages {
        stage('Stop and Remove Existing Container') {
            steps {
                script {
                    // Stop and remove existing container if it exists
                    bat "docker stop ${CONTAINER_NAME} || true"
                    bat "docker rm ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("${IMAGE_NAME}").run("--rm", "pytest")
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Run the Docker container
                    echo "Création et lancement du conteneur ${CONTAINER_NAME}."
                    bat "docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${IMAGE_NAME}"
                }
            }
        }
    }
}
