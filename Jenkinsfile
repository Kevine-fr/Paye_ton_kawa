pipeline {
    agent any

    environment {
        DOCKER_IMAGE_APP = 'client-img'
        DOCKER_IMAGE_LOCUST = 'client-logs' // Assurez-vous que ce nom est en minuscules
    }

    stages {
        stage('Build App Image') {
            steps {
                script {
                    // Construire l'image Docker de l'application
                    bat 'docker-compose build'
                }
            }
        }

        stage('Build Locust Image') {
            steps {
                script {
                    // Construire l'image Docker de Locust
                    bat "docker build -t ${DOCKER_IMAGE_LOCUST} -f Dockerfile.locust ."
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    // Exécuter les tests unitaires de l'application
                    bat 'docker-compose run app pytest'
                }
            }
        }

        stage('Start Application') {
            steps {
                script {
                    // Démarrer l'application
                    bat 'docker-compose up -d app'
                }
            }
        }

        stage('Start Locust') {
            steps {
                script {
                    // Démarrer Locust en mode headless avec les paramètres spécifiés
                    bat "docker run -d --name locust -p 8089:8089 ${DOCKER_IMAGE_LOCUST} -f locustfile.py --headless -u 10 -r 1 --run-time 1m"

                }
            }
        }

        stage('Locust Load Test') {
            steps {
                script {
                    // Attendre que Locust soit prêt
                    bat 'sleep 30'

                    // Exécuter les tests de charge Locust
                    bat 'docker exec locust locust -f locustfile.py --headless -u 10 -r 1 --run-time 1m'
                }
            }

            post {
                always {
                    echo 'Application is running on http://localhost:8000'
                    echo 'Locust is running on http://localhost:8089'
                }
            }
        }
    }
}
