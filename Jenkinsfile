pipeline {
    agent any

    environment {
        IMAGE_NAME = 'client-img'
        CONTAINER_NAME = 'Client'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        // stage('Run Tests') {
        //     steps {
        //         script {
        //             sh "docker run --rm %IMAGE_NAME% pytest"
        //         }
        //     }
        // }

        stage('Run Docker Container') {
            steps {
                script {
                    def containerExists = sh(script: "docker ps -a --format '{{.Names}}' | grep -w ${CONTAINER_NAME}", returnStatus: true) == 0

                    if (containerExists) {
                        echo "Le conteneur ${CONTAINER_NAME} existe déjà. Arrêt et suppression du conteneur existant."
                        sh "docker stop ${CONTAINER_NAME} || true"
                        sh "docker rm ${CONTAINER_NAME} || true"
                    }

                    echo "Création et lancement du conteneur ${CONTAINER_NAME}."
                    sh "docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${IMAGE_NAME}"
                }
            }
        }
    }
}
