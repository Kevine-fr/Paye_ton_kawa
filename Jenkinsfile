pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'client-image'
        DOCKER_CONTAINER = 'client-container'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Construire l'image Docker
                    bat "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Arrêter et supprimer le conteneur s'il existe déjà
                    bat "docker rm -f ${DOCKER_CONTAINER} || true"

                    // Lancer le conteneur Docker à partir de l'image construite
                    bat "docker run -d --name ${DOCKER_CONTAINER} -p 8000:8000 ${DOCKER_IMAGE}"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline terminé avec succès!'
        }
        failure {
            echo 'Échec du pipeline :('
        }
    }
}
