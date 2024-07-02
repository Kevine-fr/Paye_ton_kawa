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

        stage('Stop Unused Containers') {
            steps {
                script {
                    // Arrêter et supprimer les conteneurs inutiles
                    bat 'docker-compose down --remove-orphans'
                }
            }
        }

        stage('Start Kawa Container') {
            steps {
                script {
                    // Démarrer le conteneur Kawa qui inclut client-img et client-logs
                    bat 'docker-compose up -d'
                }
            }
        }

        stage('Locust Load Test') {
            steps {
                script {
                    // Attendre que Locust soit prêt
                    bat 'sleep 30'

                    // Exécuter les tests de charge Locust
                    bat 'docker exec locust locust -f /locustfile.py --headless -u 10 -r 1 --run-time 1m'
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
