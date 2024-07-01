pipeline {
    agent any

    environment {
        CONTAINER_NAME = "Client"
        IMAGE_NAME = "client-img"
    }

    stages {
        stage('Build and Run Docker Container') {
            steps {
                script {
                    // Vérifier si le conteneur existe
                    def containerExists = sh(script: "docker ps -a --format '{{.Names}}' | grep -w ${CONTAINER_NAME}", returnStatus: true) == 0

                    if (containerExists) {
                        echo "Le conteneur ${CONTAINER_NAME} existe déjà. Suppression du conteneur existant."
                        sh "docker rm -f ${CONTAINER_NAME}"
                    }

                    // Vérifier si l'image existe
                    def imageExists = sh(script: "docker images --format '{{.Repository}}' | grep -w ${IMAGE_NAME}", returnStatus: true) == 0

                    if (!imageExists) {
                        echo "L'image ${IMAGE_NAME} n'existe pas. Création de l'image."
                        // Construire l'image Docker à partir d'un Dockerfile dans le répertoire actuel
                        sh "docker build -t ${IMAGE_NAME} ."
                    } else {
                        echo "L'image ${IMAGE_NAME} existe déjà."
                    }

                    echo "Création et lancement du conteneur ${CONTAINER_NAME}."
                    sh "docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${IMAGE_NAME}"
                }
            }
        }
    }
}
