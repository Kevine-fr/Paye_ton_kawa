pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t client-img .'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'docker run --rm client-img sh -c "npm test"'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker run -d --name Client -p 8000:8000 client-img'
            }
        }
    }
}
