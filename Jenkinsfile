pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/csha01/RAGAs_handson.git'
            }
        }
        stage('Install') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                bat 'pytest'
            }
        }
        stage('Run') {
            steps {
                bat 'python app.py'
            }
        }
    }
}