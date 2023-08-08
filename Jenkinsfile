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
      steps {
        sh 'pip freeze'
      }
    }

    stage('Build Docker') {
      parallel {
        stage('Build Docker') {
          steps {
            sh '''docker build -t kotoracompany/smt .
'''
          }
        }

        stage('Docker Log') {
          steps {
            sh 'docker images'
          }
        }

      }
    }

    stage('') {
      steps {
        sh 'docker images'
      }
    }

  }
}