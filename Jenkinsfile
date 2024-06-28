pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'client-app' // Nom de l'image Docker à construire
        DOCKER_REGISTRY = '' // Facultatif : registre Docker si nécessaire
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Construire l'image Docker
                    def dockerImage = docker.build("${DOCKER_REGISTRY}${DOCKER_IMAGE}", "-f Dockerfile .")

                    // Publier l'image si nécessaire
                    // dockerImage.push()

                    // Afficher l'ID de l'image construite
                    echo "Image ID: ${dockerImage.id}"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Lancer le conteneur Docker à partir de l'image construite
                    docker.image("${DOCKER_REGISTRY}${DOCKER_IMAGE}").run('-p 8000:8000 --name client-container -d')
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
