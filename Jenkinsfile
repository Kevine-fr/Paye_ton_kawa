pipeline {
    agent any

    environment {
        CONTAINER_NAME = "Client"
        IMAGE_NAME = "client-img"
    }

    stages {
        stage('Check Container and Image') {
            steps {
                script {
                    // Vérifier si le conteneur existe
                    def containerExists = sh(script: "docker ps -a --format '{{.Names}}' | grep -w ${CONTAINER_NAME}", returnStatus: true) == 0

                    // Vérifier si l'image existe
                    def imageExists = sh(script: "docker images --format '{{.Repository}}' | grep -w ${IMAGE_NAME}", returnStatus: true) == 0

                    if (containerExists) {
                        echo "Le conteneur ${CONTAINER_NAME} existe déjà."

                        // Vérifier si le conteneur est en cours d'exécution
                        def containerRunning = sh(script: "docker ps --format '{{.Names}}' | grep -w ${CONTAINER_NAME}", returnStatus: true) == 0
                        if (!containerRunning) {
                            echo "Le conteneur ${CONTAINER_NAME} n'est pas en cours d'exécution. Lancement du conteneur."
                            sh "docker start ${CONTAINER_NAME}"
                        } else {
                            echo "Le conteneur ${CONTAINER_NAME} est déjà en cours d'exécution."
                        }
                    } else {
                        if (imageExists) {
                            echo "L'image ${IMAGE_NAME} existe déjà."
                        } else {
                            echo "L'image ${IMAGE_NAME} n'existe pas. Création de l'image."
                            // Construire l'image Docker à partir d'un Dockerfile dans le répertoire actuel
                            sh "docker build -t ${IMAGE_NAME} ."
                        }

                        echo "Création et lancement du conteneur ${CONTAINER_NAME}."
                        sh "docker run -d --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                    }
                }
            }
        }
    }
}