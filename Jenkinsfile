pipeline {
    agent {
        node {
            label 'Pi'
        }
    }
    stages {
        stage('Checkout Code') {
            steps {
                git(url: 'https://github.com/DuyNHKTR/PipelineSMT', branch: 'main')
            }
        }
        
        
        stage('Build Docker') {
            steps {
                sh '''docker build -t kotoracompany/smt .'''
            }
        }
        stage('Check docker image') {
            steps {
                sh 'docker images'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                sh 'docker push kotoracompany/smt'
            }
        }
    }
}
