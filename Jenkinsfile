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
                    // Vérifie si le conteneur existe déjà
                    def containerExists = docker.inside("--entrypoint='' ${IMAGE_NAME}", "docker ps -a --format '{{.Names}}' | grep -w ${CONTAINER_NAME}", returnStatus: true) == 0

                    // Si le conteneur existe, l'arrête et le supprime
                    if (containerExists) {
                        echo "Le conteneur ${CONTAINER_NAME} existe déjà. Arrêt et suppression du conteneur existant."
                        docker.stop("${CONTAINER_NAME}")
                        docker.remove("${CONTAINER_NAME}")
                    }

                    // Lance le conteneur Docker
                    echo "Création et lancement du conteneur ${CONTAINER_NAME}."
                    docker.withRun("${CONTAINER_NAME}", "--name ${CONTAINER_NAME} -p 8000:8000 ${IMAGE_NAME}")
                }
            }
        }
    }
}
