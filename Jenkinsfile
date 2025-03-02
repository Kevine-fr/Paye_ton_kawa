pipeline {
    agent any

    environment {
        DOCKER_IMAGE_APP = 'client-img'
        DOCKER_IMAGE_LOCUST = 'client-logs'
    }

    stages {
        stage('Build App Image') {
            steps {
                script {
                    catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                        bat 'docker-compose build'
                    }
                }
            }
        }

        stage('Build Locust Image') {
            steps {
                script {
                    bat "docker build -t ${DOCKER_IMAGE_LOCUST} -f Dockerfile.locust ."
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    bat 'docker-compose up -d app'
                    bat 'docker exec app pytest'
                }
            }
        }

        stage('Stop Unused Containers') {
            steps {
                script {
                    bat 'docker-compose down --remove-orphans'
                }
            }
        }

        stage('Start Kawa Container') {
            steps {
                script {
                    bat 'docker-compose up -d --no-log-prefix'
                }
            }
        }
    }
}
