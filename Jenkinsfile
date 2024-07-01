pipeline {
    agent any

    environment {
        CONTAINER_NAME = "Client"
        IMAGE_NAME = "client-img"
    }

    stages {
        stage('Remove Existing Container and Image') {
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

                    // Check if the image exists
                    def imageExists = bat(script: 'docker images -q ${IMAGE_NAME}', returnStatus: true)

                    // If the image exists, remove it
                    if (imageExists == 0) {
                        echo "L'image ${IMAGE_NAME} existe déjà. Suppression de l'image existante."
                        bat "docker rmi ${IMAGE_NAME}"
                    }
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
