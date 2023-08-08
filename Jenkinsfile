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
            sh '''docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi -f $(docker images -q)'''
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

  }
}