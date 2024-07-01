pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Stop and Remove Existing Container') {
            steps {
                script {
                    try {
                        bat 'docker stop client || echo No existing container to stop'
                        bat 'docker rm client || echo No existing container to remove'
                    } catch (Exception e) {
                        echo 'No existing container to stop or remove.'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t client .'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'docker run --rm client sh -c "npm test"'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker run -d --name client -p 8080:8080 client'
            }
        }
    }
}
