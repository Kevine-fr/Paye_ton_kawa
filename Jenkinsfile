pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Stop and Remove Existing Container') {
            steps {
                script {
                    try {
                        sh 'docker stop client || true'
                        sh 'docker rm client || true'
                    } catch (Exception e) {
                        echo "No existing container to stop or remove."
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t client-img .'
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image('client-img').inside('-v $WORKSPACE:/workspace -w /workspace') {
                        sh 'pytest tests'
                    }
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker run -d --name client -v $WORKSPACE:/workspace -w /workspace client-img'
                }
            }
        }
    }
}
