pipeline {
    agent any

    environment {
        CONTAINER_NAME = "Client"
        IMAGE_NAME = "client-img"
    }

    stages {
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
                    // Check if the container exists
                    def containerExists = bat(script: 'docker ps -a --format "{{.Names}}" | findstr /R "^' + CONTAINER_NAME + '$"', returnStatus: true)

                    // If the container exists, stop and remove it
                    if (containerExists == 0) {
                        echo "Le conteneur ${CONTAINER_NAME} existe déjà. Arrêt et suppression du conteneur existant."
                        bat "docker stop ${CONTAINER_NAME}"
                        bat "docker rm ${CONTAINER_NAME}"
                    }

                    // Run the Docker container
                    echo "Création et lancement du conteneur ${CONTAINER_NAME}."
                    bat "docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${IMAGE_NAME}"
                }
            }
        }
    }
}
