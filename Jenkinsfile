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
                script {
                    sh "docker run --rm client-img pytest"
                }
            }
        }


        stage('Run Docker Container') {
            steps {
                bat 'docker run -d --name Client -p 8000:8000 client-img'
            }
        }
    }
}
