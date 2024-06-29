pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'client-img'
        DOCKER_CONTAINER = 'Client'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Vérifier si l'image existe déjà
                    bat """
                    if not exist (docker images -q ${DOCKER_IMAGE}) (
                        docker build -t ${DOCKER_IMAGE} .
                    )
                    """
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Vérifier si le conteneur existe déjà
                    bat """
                    docker ps -a --filter "name=${DOCKER_CONTAINER}" --format "{{.ID}}" | findstr /v "^$" > nul
                    if %errorlevel% equ 0 (
                        echo "Le conteneur ${DOCKER_CONTAINER} existe déjà."
                        docker start ${DOCKER_CONTAINER}
                    ) else (
                        docker run -d --name ${DOCKER_CONTAINER} -p 8000:8000 ${DOCKER_IMAGE}
                    )
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline terminée avec succès!'
        }
        failure {
            echo 'Échec du pipeline :('
        }
    }
}
