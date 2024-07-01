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
                    try {
                        // Stop and remove existing container if it exists
                        bat(returnStatus: true, script: "docker stop ${CONTAINER_NAME}")
                        bat(returnStatus: true, script: "docker rm ${CONTAINER_NAME}")
                    } catch (Exception e) {
                        echo "Le conteneur ${CONTAINER_NAME} n'existe pas ou n'a pas pu être arrêté/effacé."
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
                    docker.image("${IMAGE_NAME}").inside("-v ${WORKSPACE}:${WORKSPACE} -w ${WORKSPACE}") {
                        bat 'pytest'
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Run the Docker container
                    echo "Création et lancement du conteneur ${CONTAINER_NAME}."
                    bat "docker run -d --name ${CONTAINER_NAME} -p 8000:8000 -v ${WORKSPACE}:${WORKSPACE} -w ${WORKSPACE} ${IMAGE_NAME}"
                }
            }
        }
    }
}
