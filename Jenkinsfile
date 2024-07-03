pipeline {
    agent any

    environment {
        DOCKER_IMAGE_APP = 'commande-img'
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


        // stage('Run Unit Tests') {
        //     steps {
        //         script {
        //             // Exécuter les tests unitaires de l'application
        //             bat 'docker-compose run app pytest'
        //         }
        //     }
        // }

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
    }
}
