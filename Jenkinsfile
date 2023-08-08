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

        stage('Run Project') {
          steps {
            sh 'python main.py'
            timeout(time: 10) {
              sh 'exit()'
            }

          }
        }

      }
    }

    stage('Build Docker') {
      parallel {
        stage('Build Docker') {
          steps {
            sh '''docker build -t SMT .
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

  }
}