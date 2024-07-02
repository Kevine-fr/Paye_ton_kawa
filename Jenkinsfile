pipeline {
    agent any

    environment {
        DOCKER_IMAGE_APP = 'client-img'
        DOCKER_IMAGE_LOCUST = 'client-logs'
    }

    stages {
        stage('Build') {
            steps {
                script {
                    // Construire les images Docker pour l'application et Locust
                    bat 'docker-compose build'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Exécuter les tests Pytest dans un conteneur Docker
                    bat 'docker-compose run app pytest'
                }
            }
        }

        stage('Start Application and Locust') {
            steps {
                script {
                    // Démarrer l'application et Locust
                    bat 'docker-compose up -d'
                }
            }
        }

        stage('Locust Load Test') {
            steps {
                script {
                    // Exécuter les tests de charge Locust
                    bat 'docker-compose run locust -f locustfile.py --headless -u 10 -r 1 --run-time 1m'
                }
            }
        }
    }

    post {
        always {
            echo 'Application is running on http://localhost:8000'
            echo 'Locust is running on http://localhost:8089'
        }
    }
}
