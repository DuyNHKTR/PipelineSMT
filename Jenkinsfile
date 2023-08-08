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

    stage('Run project') {
      parallel {
        stage('Install requirements') {
          steps {
            sh 'pip install -r requirements.txt'
          }
        }

        stage('Console Log') {
          steps {
            sh 'ls -al'
          }
        }

      }
    }

    stage('Check library version') {
      parallel {
        stage('Check library version') {
          steps {
            sh 'pip freeze'
          }
        }

        stage('Clean Node') {
          steps {
            sh 'docker rmi -f $(docker images -q)'
          }
        }

      }
    }

    stage('Build Docker') {
      steps {
        sh '''docker build -t kotoracompany/smt .
'''
      }
    }
    

    stage('Check docker image') {
      steps {
        sh 'docker images'
      }
    }
    stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'DOCKERHUB_CREDENTIALS', variable: 'DOCKERHUB_CREDENTIALS')]) {
                    sh 'docker login -u username -p $DOCKERHUB_CREDENTIALS'
                    sh 'docker push kotoracompany/smt'
                }
            }
        }

  }
}
