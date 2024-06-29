pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'client-image' // Nom de l'image Docker à construire
        DOCKER_CONTAINER = 'client-container' // Nom du conteneur Docker à lancer
        DOCKER_REGISTRY = '' // Laisser vide pour Docker Hub
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials' // ID des credentials Docker dans Jenkins
    }

    stages {
        stage('Login to Docker Registry') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CREDENTIALS_ID}") {
                        echo "Logged in to Docker Hub"
                    }
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Construire l'image Docker
                    def dockerImage = docker.build("${DOCKER_IMAGE}", "-f Dockerfile .")

                    // Publier l'image
                    dockerImage.push()

                    // Afficher l'ID de l'image construite
                    echo "Image ID: ${dockerImage.id}"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Vérifier si l'image a été créée
                    sh "docker images | grep ${DOCKER_IMAGE}"

                    // Arrêter et supprimer le conteneur s'il existe déjà
                    sh "docker rm -f ${DOCKER_CONTAINER} || true"

                    // Lancer le conteneur Docker à partir de l'image construite
                    sh "docker run -d --name ${DOCKER_CONTAINER} -p 8000:8000 ${DOCKER_IMAGE}"
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
